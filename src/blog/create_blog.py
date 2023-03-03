import boto3
import os
import json
import uuid
from datetime import datetime

region = os.environ.get('REGION')


def lambda_handler(event, context):
    try:
        if 'body' not in event or event['httpMethod'] != 'POST':
            return {
                'statusCode': 400,
                'headers': {},
                'body': json.dumps({'msg': 'Bad Request'})
            }

        table_name = os.environ.get('TABLE-NAME', 'Blogs')

        blogs_table = boto3.resource(
            'dynamodb',
            region_name=region
        )
        table = blogs_table.Table(table_name)
        blog_body = json.loads(event['body'])
        user_email = event['requestContext']['authorizer']['claims']['email']

        params = {
            'id': str(uuid.uuid4()),
            'created_at': str(datetime.timestamp(datetime.now())),
            'created_by': user_email,
            'title': blog_body['title'],
            'description': blog_body['description']
        }
        response = table.put_item(
            Item=params
        )

        #  sent mail to other users when a post is created
        sent_mail_to_other_creators(user_email)

        print(response)

        return {
            'statusCode': 201,
            'headers': {},
            'body': json.dumps({'msg': 'Blog created successfully',
                                'id': params['id']})

        }
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps(
                {'message': f'Something went wrong and we could not complete the requested action. Error:{e}'})
        }


def sent_mail_to_other_creators(user_email):
    """
    Function to sent email to other users via AWS SES when a post is created
    Returns:
    """
    user_pool_id = os.environ['USER_POOL_ID']

    # Create a CognitoIdentityProvider client
    client = boto3.client('cognito-idp', region_name=region)

    # List all users in the user pool
    response = client.list_users(
        UserPoolId=user_pool_id,
        AttributesToGet=['email']
    )

    # Extract the email addresses of all users
    email_addresses = [user['Attributes'][0]['Value'] for user in response['Users']]
    print(email_addresses)

    # Create an SES client
    ses_client = boto3.client('ses', region_name=region)

    for email_address in email_addresses:
        # Get the verification status of the email address
        response_identity = ses_client.get_identity_verification_attributes(Identities=[email_address])
        verification_status = response_identity['VerificationAttributes'][email_address]['VerificationStatus']

        # Verify the email address if it's not verified
        if verification_status != 'Success':
            response = ses_client.verify_email_identity(EmailAddress=email_address)
            print(f"Verification email sent to {email_address}. Response: {response}")
        else:
            print(f"{email_address} is already verified.")

    email_addresses.remove(user_email)

    sender = user_email
    subject = 'Hello from iBlog :)'
    body_text = 'Hey\t\n\nI just posted a new blog. Please check it out.\n\nThank you!'

    # Send the email
    if email_addresses:
        response = ses_client.send_email(
            Source=sender,
            Destination={
                'ToAddresses': email_addresses
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body_text
                    }
                }
            }
        )
