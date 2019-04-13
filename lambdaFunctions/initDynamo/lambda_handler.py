import json
import urllib.parse

from libs.aws_resource_controller import dynamoController, s3Controller


def lambda_handler(event, context):
    """
    S3にファイルがputされたときに、呼び出される
    putされたファイルの内容を元に、DynamoDBを更新する
        :param event: Lambdaに渡されるイベント情報
        :param context: Lambdaに渡されるライタイム情報
    """
    try:
        bucket = event.get("Records")[0].get("s3").get("bucket").get("name")
        key = urllib.parse.unquote_plus(
            event.get("Records")[0].get("s3").get("object").get("key"), encoding="utf-8"
        )

        print("[bucket]: " + bucket + " [key]: " + key)
        response = s3Controller().getObject(bucket, key)
        coupons = json.loads(response.get("Body").read())

        for coupon in coupons:
            dynamoController().putItem(coupon)
        print("Put Success")
    except Exception as e:
        print("Put Failed:", e)
        raise e
