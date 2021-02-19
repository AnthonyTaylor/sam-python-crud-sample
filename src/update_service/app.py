import boto3
import os
import json


def lambda_handler(message, context):

    if ('body' not in message or
            message['httpMethod'] != 'PUT'):
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
    service = json.loads(message['body'])

    params = {
        'id': service['id']
    }

    response = table.update_item(
        Key=params,
        UpdateExpression="set url = :u, previous_response = :p",
        ExpressionAttributeValues={
            ':u': service['url'],
            ':p': service['previous_response']
        },
        ReturnValues="UPDATED_NEW"
    )
    # print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'service updated'})
    }
