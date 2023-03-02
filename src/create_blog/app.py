import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(event, context):
    if 'body' not in event or event['httpMethod'] != 'POST':
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE-NAME', 'Blogs')
    region = os.environ.get('REGION')

    blogs_table = boto3.resource(
        'dynamodb',
        region_name=region
    )
    table = blogs_table.Table(table_name)
    blog_body = json.loads(event['body'])

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
        'body': json.dumps({'msg': 'Blog created successfully'})
    }
