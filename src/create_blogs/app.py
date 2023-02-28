import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(message, context):
    if 'body' not in message or message['httpMethod'] != 'POST':
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'Blogs')
    region = os.environ.get('REGION', 'us-east-1')

    print(region, table_name)

    blogs_table = boto3.resource(
        'dynamodb',
        region_name=region
    )
    table = blogs_table.Table(table_name)
    blog_body = json.loads(message['body'])
    print(blog_body)

    params = {
        'id': str(uuid.uuid4()),
        'created_at': str(datetime.timestamp(datetime.now())),
        'title': blog_body['title'],
        'description': blog_body['description']
    }

    response = table.put_item(
        Item=params
    )

    print(response)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'msg': 'Blog created'})
    }
