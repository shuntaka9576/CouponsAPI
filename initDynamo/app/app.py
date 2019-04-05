import os
import json
import boto3
import urllib.parse

if os.getenv("AWS_SAM_LOCAL"):
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://host.docker.internal:4569/'
    )
    s3 = boto3.client(
        's3',
        endpoint_url='http://host.docker.internal:4572/'
    )
else:
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("[bucket]: " + bucket + " [key]: " + key)

    response = s3.get_object(Bucket=bucket, Key=key)
    coupons = json.loads(response['Body'].read())
    table = dynamodb.Table('coupons')
    try:
        for coupon in coupons:
            table.put_item(
                Item=coupon
            )
            print("Put Success")
        return
    except Exception as e:
        print("Put Failed")
        print(e)
        return
