import base64
import os
import json
import boto3

s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:

        bucket_name = os.environ['BUCKET_NAME']
        file_content = base64.b64decode(event['body'])
        file_name = event['pathParameters']['filename']
        blog_id = event['pathParameters']['blog_id']

        # s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        s3.put_object(Bucket=bucket_name, Key=blog_id, Body=file_content)

        # map the attachment into dynamodb Blogs table
        # For now i put the filename as the corresponding blogs uuid

        response = {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded successfully"})
        }

        return response
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps(
                {'message': f'Something went wrong and we could not complete the requested action. Error:{e}'})
        }
