import json

from tests.fixture import couponTestDatas, initDb

from couponsApi.getList.lambda_handler import lambda_handler


def test_lambda_handler_get(initDb):
    """ getListのlambda_handlerのテスト関数
    HTTPメソッド分岐処理を中心にテスト
    """
    testDatas = [couponTestDatas[couponKey] for couponKey in couponTestDatas]

    tests = [
        {
            "name": "GET クーポン一覧問合せ",
            "case": "normal",
            "input": {
                "httpMethod": "GET",
                "path": "/coupons",
                "body": None,
                "queryStringParameters": None,
            },
            "expect": {
                "status": 200,
                "body": {
                    "header": {"status": "Success", "errors": []},
                    "response": {"coupons": testDatas},
                },
            },
        },
        {
            "name": "GET 期間問い合せ(id:0001246)",
            "case": "normal",
            "input": {
                "httpMethod": "GET",
                "path": "/coupons",
                "body": None,
                "queryStringParameters": {
                    "startdate": "20180401",
                    "enddate": "20180501",
                },
            },
            "expect": {
                "status": 200,
                "body": {
                    "header": {"status": "Success", "errors": []},
                    "response": {"coupons": [couponTestDatas["0001246"]]},
                },
            },
        },
        {
            "name": "POST クーポン一覧問合せ",
            "case": "normal",
            "input": {
                "httpMethod": "POST",
                "path": "/coupons",
                "body": None,
                "queryStringParameters": None,
            },
            "expect": {
                "status": 200,
                "body": {
                    "header": {"status": "Success", "errors": []},
                    "response": {"coupons": testDatas},
                },
            },
        },
        {
            "name": "POST 期間問い合せ(id:0001246)",
            "case": "normal",
            "input": {
                "httpMethod": "POST",
                "path": "/coupons",
                "body": '{"startdate":"20180401","enddate":"20180501"}',
                "queryStringParameters": None,
            },
            "expect": {
                "status": 200,
                "body": {
                    "header": {"status": "Success", "errors": []},
                    "response": {"coupons": [couponTestDatas["0001246"]]},
                },
            },
        },
        {
            "name": "POST 期間問合せ(不正Bodyメッセージ)",
            "case": "normal",
            "input": {
                "httpMethod": "POST",
                "path": "/coupons",
                "body": '{"startdate":"20180401","enddate","20180501"}',
                "queryStringParameters": None,
            },
            "expect": {
                "status": 400,
                "body": {
                    "header": {
                        "status": "Error",
                        "errors": [
                            {"filed": "POST Body", "message": "POST body parse error"}
                        ],
                    }
                },
            },
        },
        {
            "name": "サポートされていないメソッド問い合せ",
            "case": "normal",
            "input": {"startdate": "20190401", "enddate": "20190101"},
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
