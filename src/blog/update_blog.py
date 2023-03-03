import boto3
import os
import json

from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    try:
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

        # Only post-creator also has the option to Update the post.
        user_email = event['requestContext']['authorizer']['claims']['email']
        post_creator = table.get_item(Key=params)['Item']['created_by']
        print(post_creator)

        if user_email != post_creator:
            return {
                'statusCode': 403,
                'headers': {},
                'body': json.dumps(
                    {'message': "You don't have the permission to update this post. Only post creator can update!!"})
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
            'body': json.dumps({'message': 'Blog updated successfully'})
        }
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps(
                {'message': f'Something went wrong and we could not complete the requested action. Error:{e}'})
        }
