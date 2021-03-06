import json

import boto3
from botocore.config import Config
from tests.fixture import couponTestDatas, initDb

from couponsApi.getId.getId_controller import GetIdController


class TestGetIdController:
    def test_handler(self, initDb):
        """ /coupons/{id}のControllerロジックのテスト
        """
        tests = [
            {
                "name": "クーポンID(0001245)の問合せ",
                "case": "normal",
                "input": {"id": "0001245"},
                "expect": {
                    "status": 200,
                    "body": {
                        "header": {"status": "Success", "errors": []},
                        "response": {"coupons": [couponTestDatas["0001245"]]},
                    },
                },
            },
            {
                "name": "クーポンID(0001246)の問合せ",
                "case": "normal",
                "input": {"id": "0001246"},
                "expect": {
                    "status": 200,
                    "body": {
                        "header": {"status": "Success", "errors": []},
                        "response": {"coupons": [couponTestDatas["0001246"]]},
                    },
                },
            },
            {
                "name": "サポートされていないクーポンIDの問合せ",
                "case": "normal",
                "input": {"id": "1"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {"field": "id", "message": "Unsupported coupon id"}
                            ],
                        }
                    },
                },
            },
            {
                "name": "パラメータidのvalueに数値以外を指定した問合せ",
                "case": "normal",
                "input": {"id": "zero"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "field": "id",
                                    "message": "value does not match regex '[0-9].*'",
                                }
                            ],
                        }
                    },
                },
            },
        ]

        for test in tests:
            result = GetIdController().handler(test["input"])

            assert result["statusCode"] == test["expect"]["status"]
            assert json.loads(result["body"]) == test["expect"]["body"]

    def test_handler_internalServerError(self):
        """ dynamodbデータ取得処理で異常があった場合
        指定した宛先は、LISTENしていないポートを指定
        """
        test = {
            "input": {"id": "0001246"},
            "expect": {
                "name": "データソースとの接続がタイムアウトしたときの問合せ",
                "case": "normal",
                "status": 500,
                "body": {
                    "header": {
                        "status": "Error",
                        "errors": [{"message": "Intenal server error"}],
                    }
                },
            },
        }
        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://localhost:9999/", config=config
        )
        result = GetIdController().handler(test["input"], obj=dynamodb)

        assert result["statusCode"] == test["expect"]["status"]
        assert json.loads(result["body"]) == test["expect"]["body"]
