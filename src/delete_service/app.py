import boto3
import os
import json


def lambda_handler(message, context):

    if ('pathParameters' not in message or
            message['httpMethod'] != 'DELETE'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'Services')
    region = os.environ.get('REGION', 'eu-west-2')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    if aws_environment == 'AWS_SAM_LOCAL':
        Services_table = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb:8000'
        )
    else:
        Services_table = boto3.resource(
            'dynamodb',
            region_name=region
        )

    table = Services_table.Table(table_name)
    activity_id = message['pathParameters']['id']


    params = {
        'id': activity_id,
    }

    response = table.delete_item(
        Key=params
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'Service deleted'})
    }
