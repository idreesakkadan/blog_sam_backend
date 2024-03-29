import json
import os
import boto3


def lambda_handler(event, context):
    try:
        if 'httpMethod' not in event or event['httpMethod'] != 'GET':
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

        response = table.scan()
        print(response)

        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps(
                {'message': f'Something went wrong and we could not complete the requested action. Error:{e}'})
        }