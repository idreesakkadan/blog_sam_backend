import boto3
import os
import json


def lambda_handler(event, context):

    if 'pathParameters' not in event or event['httpMethod'] != 'DELETE':
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE-NAME', 'Blogs')
    region = os.environ.get('REGION', 'us-east-1')

    blogs_table = boto3.resource(
        'dynamodb',
        region_name=region
    )

    table = blogs_table.Table(table_name)
    blog_id = event['pathParameters']['id']

    params = {
        'id': blog_id
    }

    response = table.delete_item(
        Key=params
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'Blog deleted successfully'})
    }
