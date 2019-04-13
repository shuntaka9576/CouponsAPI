import json

import pytest
from tests.fixture import couponTestDatas, initDb

from couponsApi.getId.lambda_handler import lambda_handler


def test_lambda_handler_get(initDb):
    """getIdのlambda_handlerのテスト関数
    """

    tests = [
        {
            "name": "GET /coupons/0001245 Success",
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
            "name": "POST",
            "case": "normal",
            "input": {
                "httpMethod": "POST",
                "path": "/coupons",
                "body": '{"id", "0001245"}',
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
            "name": "POST body empty error",
            "case": "normal",
            "input": {"httpMethod": "POST", "body": None, "pathParameters": None},
            "expect": {
                "status": 400,
                "body": {
                    "header": {
                        "status": "Error",
                        "errors": [
                            {"filed": "POST Body", "message": "POST body empty"}
                        ],
                    }
                },
            },
        },
        {
            "name": "POST body parse error",
            "case": "normal",
            "input": {
                "httpMethod": "POST",
                "path": "/coupons",
                "body": '{"id", "0001245"}',
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
            "name": "Unsupported HTTP method",
            "case": "non-normal",
            "input": {
                "httpMethod": "HEAD",
                "body": '{"id": "0001245"}',
                "pathParameters": None,
            },
            "expect": {"Exception": SystemExit, "exitCode": 1},
        },
    ]

    for test in tests:
        if test.get("case") == "non-normal":
            with pytest.raises(test.get("expect").get("Exception")) as pytest_wrapped_e:
                lambda_handler(test.get("input"), {})

            assert pytest_wrapped_e.type == test.get("expect").get("Exception")
            assert pytest_wrapped_e.value.code == test.get("expect").get("exitCode")

        else:
            result = lambda_handler(test.get("input"), {})
            expectCode = test.get("expect").get("status")
            expectRes = test.get("expect").get("body")

            assert result.get("statusCode") == expectCode
            assert json.loads(result.get("body")) == expectRes
