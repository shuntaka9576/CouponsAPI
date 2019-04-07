import boto3
import os
import pytest
import termcolor

couponTestDatas = [{
    "id": "0001245",
    "title": "全商品 10% OFF !",
    "explain": "ご利用一回限り。他のクーポンとの併用はできません。クーポンをご利用いただいた場合、ポイントはつきません。",
    "coupon-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/coupon/0001245.png",
    "qr-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/qr/0001245.jpg",
    "start-date": "20190401",
    "end-date": "20190901"
}, {
    "id": "0001246",
    "title": "全商品 5% OFF !",
    "explain": "何回でも利用可能。他のクーポンとの併用はできません。クーポンをご利用いただいた場合、ポイントはつきません。",
    "coupon-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/coupon/0001246.png",
    "qr-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/qr/0001246.jpg",
    "start-date": "20180401",
    "end-date": "20180901"
}]

if os.getenv("AWS_SAM_LOCAL"):
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:4569/'
    )
    s3 = boto3.client(
        's3',
        endpoint_url='http://localhost:4573/'
    )
else:
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')


@pytest.fixture(scope="function", autouse=True)
def initS3():
    return


@pytest.fixture(scope="function", autouse=True)
def initdb():
    # テストデータを投入
    table = dynamodb.Table("coupons")
    for coupon in couponTestDatas:
        table.put_item(
            Item=coupon
        )
    yield print(termcolor.colored("PutDB[OK] ", "green"), end="")

    # テストコード実行後、テーブルをtruncate
    for coupon in couponTestDatas:
        table.delete_item(
            Key={
                'id': coupon["id"]
            })

    res = table.scan()
    if res["Count"] == 0:
        print(termcolor.colored(" clearDB[OK] ", "green"), end="")
    else:
        raise Exception
