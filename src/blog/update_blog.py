import boto3
import os
import json


def lambda_handler(event, context):
    try:
        # TODO : Only post-creator also has the option to Update the post.
        print("event:", event, "context:", context)
        if 'body' not in event or event['httpMethod'] != 'PUT':
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
        blog_body = json.loads(event['body'])

        params = {
            'id': blog_id
        }

        response = table.update_item(
            Key=params,
            ConditionExpression='attribute_exists(id)',
            UpdateExpression="set title = :title, description = :desc",
            ExpressionAttributeValues={
                ':title': blog_body['title'],
                ':desc': blog_body['description']
            },
            ReturnValues="UPDATED_NEW"
        )
        print(response)

        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({'msg': 'Blog updated successfully'})
        }
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps(
                {'message': f'Something went wrong and we could not complete the requested action. Error:{e}'})
        }
