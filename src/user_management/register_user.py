import boto3
import os

CLIENT_ID = os.environ.get('USER_POOL_CLIENT_ID')

# not using for now: Using cognito hosted ui for signup


def lambda_handler(event, context):
    for field in ["email", "password", "name"]:
        if not event.get(field):
            return {'message': f"{field} is not present"}

    email = event["email"]
    password = event['password']
    name = event["name"]

    client = boto3.client('cognito-idp')
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': "name",
                    'Value': name
                },
                {
                    'Name': "email",
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': email
                },
                {
                    'Name': "custom:username",
                    'Value': email
                }
            ])

    except client.exceptions.UsernameExistsException as e:
        return {
            "message": "This username already exists"
        }
    except client.exceptions.InvalidPasswordException as e:
        return {
            "message": "Password should have Caps, Special chars, Numbers"
        }
    except client.exceptions.UserLambdaValidationException as e:
        return {
            "message": "Email already exists"
        }

    except Exception as e:
        return {
            "message": str(e),
        }

    return {
            "message": "Please confirm your signup, check Email for validation code",
        }
