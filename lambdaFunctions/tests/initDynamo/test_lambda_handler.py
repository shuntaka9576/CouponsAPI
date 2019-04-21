import pytest

from initDynamo.lambda_handler import lambda_handler
from tests.fixture import initS3


def test_lambda_handler(initS3):
    """ initDynamoのlambda_handlerのテスト関数
    正常系は以下のデータ比較し、パスすることを確認する
        expect: ./testdata/initDbData.json
        result: Dynamodbのデータ
    """

    tests = [
        {
            "name": "正常系",
            "case": "normal",
            "input": {
                "Records": [
                    {
                        "s3": {
                            "bucket": {"name": "dev-cpa-s3-coupons"},
                            "object": {"key": "dynamo/initDbData.json"},
                        }
                    }
                ]
            },
        },
        {
            "name": "存在しないファイルのイベントがきた場合",
            "case": "non-normal",
            "input": {
                "Records": [
                    {
                        "s3": {
                            "bucket": {"name": "dev-cpa-s3-coupons"},
                            "object": {"key": "dynamodb/notfound.json"},
                        }
                    }
                ]
            },
            "expect": "Put Success",
        },
    ]

    for test in tests:
        if test["case"] == "non-normal":
            with pytest.raises(Exception):
                lambda_handler(test["input"], {})
        else:
            lambda_handler(test["input"], {})
