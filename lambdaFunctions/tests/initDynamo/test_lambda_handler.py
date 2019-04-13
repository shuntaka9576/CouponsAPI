import pytest
from tests.fixture import initS3


def test_lambda_handler(initS3):
    from initDynamo.lambda_handler import lambda_handler

    """
    正常系は以下のデータ比較し、パスすることを確認する
        expect: ./testdata/initDbData.json
        result: Dynamodbのデータ
    """
    tests = [
        {
            "name": "success",
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
            "expect": "",
        },
        {
            "name": "empty key Records",
            "case": "non-normal",
            "input": {"Records": []},
            "expect": "",
        },
        {
            "name": "not found s3 file object",
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
        if test.get("case") == "non-normal":
            with pytest.raises(Exception):
                lambda_handler(test.get("input"), {})
        else:
            # Exceptionが起きなければ、パス
            lambda_handler(test.get("input"), {})
