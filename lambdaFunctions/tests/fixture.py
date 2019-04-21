import os

import boto3
import pytest
import termcolor

# テスト時に利用するクーポンデータ
couponTestDatas = {
    "0001245": {
        "id": "0001245",
        "title": "全商品 10% OFF !",
        "explain": "ご利用一回限り。他のクーポンとの併用はできません。クーポンをご利用いただいた場合、ポイントはつきません。",
        "coupon-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/coupon/0001245.png",
        "qr-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/qr/0001245.jpg",
        "start-date": "20190401",
        "end-date": "20190501",
    },
    "0001246": {
        "id": "0001246",
        "title": "全商品 5% OFF !",
        "explain": "何回でも利用可能。他のクーポンとの併用はできません。クーポンをご利用いただいた場合、ポイントはつきません。",
        "coupon-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/coupon/0001246.png",
        "qr-image": "https://s3-ap-northeast-1.amazonaws.com/dev-cpa-s3-materials/qr/0001246.jpg",
        "start-date": "20180401",
        "end-date": "20180501",
    },
}


# 環境変数でLocalstackとawsで宛先を変更
if os.getenv("AWS_SAM_LOCAL"):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4569/")
    s3 = boto3.client("s3", endpoint_url="http://localhost:4572/")
    couponsBucket = boto3.resource("s3", endpoint_url="http://localhost:4572/").Bucket(
        "dev-cpa-s3-coupons"
    )
else:
    dynamodb = boto3.resource("dynamodb")
    s3 = boto3.client("s3")
    couponsBucket = boto3.resource("s3").Bucket("dev-cpa-s3-coupons")


@pytest.fixture(scope="function")
def initS3():
    """
    テスト前処理
    """
    # Lambdaが参照するテストデータをS3にアップロード
    putFilePath = os.path.join(os.getcwd(), "tests", "testdata", "initDbData.json")
    couponsBucket.upload_file(putFilePath, "dynamo/initDbData.json")
    yield print(termcolor.colored("PutS3[OK] ", "green"), end="")

    """
    テスト後処理
    """
    # S3にアップロードしたテストデータを削除
    for key in couponsBucket.objects.all():
        key.delete()

    print(termcolor.colored(" ClearS3[OK] ", "green"), end="")


@pytest.fixture(scope="function")
def initDb():
    table = dynamodb.Table("coupons")

    """
    テスト前処理
    """
    # テーブルデータをtruncate
    for couponKey in couponTestDatas:
        table.delete_item(Key={"id": couponTestDatas[couponKey]["id"]})

    # テストデータを投入
    for couponKey in couponTestDatas:
        table.put_item(Item=couponTestDatas[couponKey])

    yield print(termcolor.colored("PutDB[OK] ", "green"), end="")

    """
    テスト後処理
    """
    # テストコード実行後、テーブルをtruncate
    for couponKey in couponTestDatas:
        table.delete_item(Key={"id": couponTestDatas[couponKey]["id"]})
    res = table.scan()

    if res["Count"] == 0:
        print(termcolor.colored(" clearDB[OK] ", "green"), end="")
    else:
        raise Exception
