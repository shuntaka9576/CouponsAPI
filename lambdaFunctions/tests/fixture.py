import pytest
import os
import boto3

couponTestDatas = [{
    "id": "0001245",
    "title": "全商品 10% OFF !",
    "explain": "ご利用一回限り。他のクーポンとの併用はできません。クーポンをご利用いただいた場合、ポイントはつきません。",
    "coupon-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/coupon/0001245.png",
    "qr-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/qr/0001245.jpg"
}, {
    "id": "0001246",
    "title": "全商品 5% OFF !",
    "explain": "何回でも利用可能。他のクーポンとの併用はできません。クーポンをご利用いただいた場合、ポイントはつきません。",
    "coupon-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/coupon/0001246.png",
    "qr-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/qr/0001246.jpg"
}]


@pytest.fixture(scope="function", autouse=True)
def initdb():
    if os.getenv("AWS_SAM_LOCAL"):
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url="http://localhost:4569/"
        )
    else:
        dynamodb = boto3.resource("dynamodb")

    try:
        for coupon in couponTestDatas:
            table = dynamodb.Table("coupons")
            table.put_item(
                Item=coupon
            )
    except Exception as e:
        print(e)
