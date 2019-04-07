import json
import urllib.parse
from libs.aws_resource_controller import s3Controller, dynamoController


def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        print("[bucket]: " + bucket + " [key]: " + key)

        response = s3Controller().s3.get_object(Bucket=bucket, Key=key)
        coupons = json.loads(response['Body'].read())
        for coupon in coupons:
            dynamoController().putItem(coupon)
        print("Put Success")
        return
    except Exception as e:
        print("Put Failed:", e)
        raise e
