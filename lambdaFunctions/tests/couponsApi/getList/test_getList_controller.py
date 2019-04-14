import json

import boto3
from botocore.config import Config
from tests.fixture import couponTestDatas, initDb, initS3

from couponsApi.getList.getList_controller import GetListController


class TestGetListController:
    def test_queryHandler(self, initDb):
        tests = [
            {
                "name": "check couponCode[0001246]",
                "case": "normal",
                "input": {"startdate": "20180401", "enddate": "20180501"},
                "expect": {
                    "status": 200,
                    "body": {
                        "header": {"status": "Success", "errors": []},
                        "response": {"coupons": [couponTestDatas["0001246"]]},
                    },
                },
            },
            {
                "name": "check couponCode[0001245]",
                "case": "normal",
                "input": {"startdate": "20190401", "enddate": "20190501"},
                "expect": {
                    "status": 200,
                    "body": {
                        "header": {"status": "Success", "errors": []},
                        "response": {"coupons": [couponTestDatas["0001245"]]},
                    },
                },
            },
            {
                "name": "check long duration",
                "case": "normal",
                "input": {"startdate": "20180401", "enddate": "20190501"},
                "expect": {
                    "status": 200,
                    "body": {
                        "header": {"status": "Success", "errors": []},
                        "response": {"coupons": []},
                    },
                },
            },
            {
                "name": "Request today available coupon",
                "case": "normal",
                "input": {"startdate": "20180401", "enddate": "20180401"},
                "expect": {
                    "status": 200,
                    "body": {
                        "header": {"status": "Success", "errors": []},
                        "response": {"coupons": [couponTestDatas["0001246"]]},
                    },
                },
            },
            {
                "name": "invalid date value",
                "case": "normal",
                "input": {"startdate": "2019/04/08", "enddate": "2019/05/04"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "field": "enddate",
                                    "message": "value does not match regex '[0-9]{8}'",
                                },
                                {
                                    "field": "startdate",
                                    "message": "value does not match regex '[0-9]{8}'",
                                },
                            ],
                        }
                    },
                },
            },
            {
                "name": "invalid date value",
                "case": "normal",
                "input": {"startdate": "2019-04-08", "enddate": "2019-05-04"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "field": "enddate",
                                    "message": "value does not match regex '[0-9]{8}'",
                                },
                                {
                                    "field": "startdate",
                                    "message": "value does not match regex '[0-9]{8}'",
                                },
                            ],
                        }
                    },
                },
            },
            {
                "name": "Nonexistent startdate",
                "case": "normal",
                "input": {"startdate": "20180431", "enddate": "20190501"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {"filed": "startdate", "message": "incorrect as date"}
                            ],
                        }
                    },
                },
            },
            {
                "name": "Nonexistent enddate",
                "case": "normal",
                "input": {"startdate": "20180401", "enddate": "20190431"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {"filed": "enddate", "message": "incorrect as date"}
                            ],
                        }
                    },
                },
            },
            {
                "name": "Nonexistent startdate and enddate",
                "case": "normal",
                "input": {"startdate": "20180431", "enddate": "20190432"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {"filed": "startdate", "message": "incorrect as date"},
                                {"filed": "enddate", "message": "incorrect as date"},
                            ],
                        }
                    },
                },
            },
            {
                "name": "startdate is more than enddate",
                "case": "normal",
                "input": {"startdate": "20190401", "enddate": "20190101"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "filed": "startdate",
                                    "message": "startdate later than enddate",
                                }
                            ],
                        }
                    },
                },
            },
        ]

        for test in tests:
            result = GetListController().queryHandler(test["input"])

            assert result["statusCode"] == test["expect"]["status"]
            assert json.loads(result["body"]) == test["expect"]["body"]

    def test_queryHandler_internalServerError(self):
        """dynamodbデータ取得処理で異常があった場合
        指定した宛先は、LISTENしていないポートを指定
        """
        input = {"startdate": "20180401", "enddate": "20180501"}
        expect = {
            "status": 500,
            "body": {
                "header": {
                    "status": "Error",
                    "errors": [{"message": "Intenal server error"}],
                }
            },
        }
        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://localhost:9999/", config=config
        )
        result = GetListController().queryHandler(input, obj=dynamodb)

        assert result["statusCode"] == expect["status"]
        assert json.loads(result["body"]) == expect["body"]

    def test_pathHandler(self, initDb):
        testDatas = [couponTestDatas[couponKey] for couponKey in couponTestDatas]
        tests = [
            {
                "name": "valid path(/coupons)",
                "input": {"path": "/coupons"},
                "expect": {
                    "status": 200,
                    "body": {
                        "header": {"status": "Success", "errors": []},
                        "response": {"coupons": testDatas},
                    },
                },
            },
            {
                "name": "invalid path(/couponss)",
                "input": {"path": "/couponss"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "field": "path",
                                    "message": "value does not match regex '/coupons'",
                                }
                            ],
                        }
                    },
                },
            },
        ]

        for test in tests:
            result = GetListController().pathHandler(test["input"])
            assert result["statusCode"] == test["expect"]["status"]
            assert json.loads(result["body"]) == test["expect"]["body"]

    def test_pathHandler_internalServerError(self):
        """dynamodbデータ取得処理で異常があった場合
        指定した宛先は、LISTENしていないポートを指定
        """
        input = {"path": "/coupons"}
        expect = {
            "status": 500,
            "body": {
                "header": {
                    "status": "Error",
                    "errors": [{"message": "Intenal server error"}],
                }
            },
        }
        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://localhost:9999/", config=config
        )
        result = GetListController().pathHandler(input, obj=dynamodb)

        assert result["statusCode"] == expect["status"]
        assert json.loads(result["body"]) == expect["body"]
