import json
import os
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    if 'pathParameters' not in event or event['httpMethod'] != 'GET':
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE_NAME', 'Blogs')
    region = os.environ.get('REGION')

    blogs_table = boto3.resource(
        'dynamodb',
        region_name=region
    )

    table = blogs_table.Table(table_name)
    blog_id = event['pathParameters']['id']

    response = table.query(
        KeyConditionExpression=Key('id').eq(blog_id)
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
