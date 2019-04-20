import json

import boto3
from botocore.config import Config
from tests.fixture import couponTestDatas, initDb

from couponsApi.getList.getList_controller import GetListController


class TestGetListController:
    def test_pathHandler(self, initDb):
        """ /coupons(期間問い合せなし)のControllerロジックのテスト
        """
        testDatas = [couponTestDatas[couponKey] for couponKey in couponTestDatas]
        # 現在はApigatewayでトリガーされないので不要
        tests = [
            {
                "name": "正常系",
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
                "name": "パス名不正",
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

    def test_queryHandler(self, initDb):
        """ /coupons(期間問い合せあり)のControllerロジックのテスト
        """
        tests = [
            {
                "name": "id:0001245の期間問い合せ",
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
                "name": "id:0001246の期間問い合せ",
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
                "name": "期間が長く該当idがない",
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
                "name": "その日に使えるクーポン検索",
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
                "name": "日付指定不正(yyyy/mm/dd)",
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
                "name": "日付指定不正(yyyy-mm-dd)",
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
                "name": "startdateに存在しない日付指定",
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
                "name": "enddateに存在しない日付指定",
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
                "name": "startdate,enddateに存在しない日付指定",
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
                "name": "存在しない期間を指定",
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
