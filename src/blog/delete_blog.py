import boto3
import os
import json


def lambda_handler(event, context):

    try:
        if 'pathParameters' not in event or event['httpMethod'] != 'DELETE':
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
        blog_id = event['pathParameters']['id']

        params = {
            'id': blog_id
        }

        # Only post-creator also has the option to delete the post.
        user_email = event['requestContext']['authorizer']['claims']['email']
        post_creator = table.get_item(Key=params)['Item']['created_by']
        print(post_creator)

        if user_email != post_creator:
            return {
                'statusCode': 403,
                'headers': {},
                'body': json.dumps(
                    {'message': "You don't have the permission to delete this post. Only post creator can delete!!"})
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
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps(
                {'message': f'Something went wrong and we could not complete the requested action. Error:{e}'})
        }
