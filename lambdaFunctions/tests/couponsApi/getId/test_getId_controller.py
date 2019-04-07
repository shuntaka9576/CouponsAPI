import json

from tests.fixture import couponTestDatas, initDb

from couponsApi.getId.getId_controller import GetIdController


class TestGetIdController:
    def test_handler(self, initDb):
        tests = [
            {
                "name": "Request 0001245",
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
                "name": "Request 0001246",
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
                "name": "Unsupported coupons id",
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
                "name": "invalid value",
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
            result = GetIdController().handler(test.get("input"))
            expectCode = test.get("expect").get("status")
            expectRes = test.get("expect").get("body")

            assert result.get("statusCode") == expectCode
            assert json.loads(result.get("body")) == expectRes
