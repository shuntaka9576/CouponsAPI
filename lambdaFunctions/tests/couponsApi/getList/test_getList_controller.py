import json

from couponsApi.getList.getList_controller import GetListController
from tests.fixture import couponTestDatas, initDb


class TestGetListController:
    def test_queryHandler(self, initDb):
        tests = [
            {
                "name": "check couponCode[0001246]",
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
                "name": "startdate is more than enddate",
                "input": {"startdate": "20190401", "enddate": "20190101"},
                "expect": {
                    "status": 400,
                    "body": {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "filed": "start-date",
                                    "message": "period that does not exist",
                                }
                            ],
                        }
                    },
                },
            },
        ]

        for test in tests:
            result = GetListController().queryHandler(test.get("input"))
            expectCode = test.get("expect").get("status")
            expectRes = test.get("expect").get("body")

            assert result.get("statusCode") == expectCode
            assert json.loads(result.get("body")) == expectRes

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
            result = GetListController().pathHandler(test.get("input"))
            expectCode = test.get("expect").get("status")
            expectRes = test.get("expect").get("body")
            assert result.get("statusCode") == expectCode
            assert json.loads(result.get("body")) == expectRes
