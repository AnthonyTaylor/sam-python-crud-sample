import boto3
import os
import json


def lambda_handler(message, context):

    if ('httpMethod' not in message or
            message['httpMethod'] != 'GET'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'Services')
    region = os.environ.get('REGION', 'eu-west-2')
    aws_environment = os.environ.get('AWSENV', 'AWS_SAM_LOCAL')
    # stage = os.environ.get('STAGE', ' dev)
    # if aws_environment == 'AWS_SAM_LOCAL':
    if True:
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

    response = table.scan()
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }