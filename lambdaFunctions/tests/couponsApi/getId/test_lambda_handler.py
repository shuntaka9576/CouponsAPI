import json

from tests.fixture import couponTestDatas, initDb

from couponsApi.getId.lambda_handler import lambda_handler


def test_lambda_handler_get(initDb):
    """getIdのlambda_handlerのテスト関数
    HTTPメソッド分岐処理を中心にテスト
    """
    tests = [
        {
            "name": "クーポンID(0001245)の問合せ",
            "case": "normal",
            "input": {
                "httpMethod": "GET",
                "body": None,
                "pathParameters": {"id": "0001245"},
            },
            "expect": {
                "status": 200,
                "body": {
                    "header": {"status": "Success", "errors": []},
                    "response": {"coupons": [couponTestDatas["0001245"]]},
                },
            },
        },
        {
            "name": "サポートされていないクーポンIDの問合せ",
            "case": "normal",
            "input": {
                "httpMethod": "HEAD",
                "body": '{"id": "0001245"}',
                "pathParameters": None,
            },
            "expect": {
                "status": 405,
                "body": {
                    "header": {
                        "status": "Error",
                        "errors": [{"message": "Unsupported method"}],
                    }
                },
            },
        },
    ]

    for test in tests:
        result = lambda_handler(test["input"], {})

        assert result["statusCode"] == test["expect"]["status"]
        assert json.loads(result["body"]) == test["expect"]["body"]
