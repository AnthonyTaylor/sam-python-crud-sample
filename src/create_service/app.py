import boto3
import os
import json
import uuid
from datetime import datetime
from pprint import pprint


def lambda_handler(message, context):
    if ('body' not in message or
            message['httpMethod'] != 'POST'):
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
    website = json.loads(message['body'])

    params = {
        'id': str(uuid.uuid4()),
        'url': website['url'],
        'previous_response': website['previous_response']
    }

    response = table.put_item(
        TableName=table_name,
        Item=params
    )

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id": params['id']})
    }
