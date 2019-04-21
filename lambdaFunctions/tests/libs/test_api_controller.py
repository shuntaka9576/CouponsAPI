from libs.api_controller import Controller


class TestController:
    def test_ok(self):
        tests = [
            {
                "name": "single byte character",
                "case": "normal",
                "input": {"status": "Success"},
                "expect": {
                    "statusCode": 200,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "Success"}',
                },
            },
            {
                "name": "multi byte character",
                "case": "normal",
                "input": {"status": "成功"},
                "expect": {
                    "statusCode": 200,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "成功"}',
                },
            },
        ]

        for test in tests:
            result = Controller().ok(test["input"])

            assert result == test["expect"]

    def test_bad(self):
        tests = [
            {
                "name": "single byte character",
                "case": "normal",
                "input": {"status": "Success"},
                "expect": {
                    "statusCode": 400,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "Success"}',
                },
            },
            {
                "name": "multi byte character",
                "case": "normal",
                "input": {"status": "成功"},
                "expect": {
                    "statusCode": 400,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "成功"}',
                },
            },
        ]

        for test in tests:
            result = Controller().bad(test["input"])

            assert result == test["expect"]

    def test_methodNotAllowed(self):
        tests = [
            {
                "name": "single byte character",
                "case": "normal",
                "input": {"status": "Success"},
                "expect": {
                    "statusCode": 405,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "Success"}',
                },
            },
            {
                "name": "multi byte character",
                "case": "normal",
                "input": {"status": "成功"},
                "expect": {
                    "statusCode": 405,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "成功"}',
                },
            },
        ]

        for test in tests:
            result = Controller().methodNotAllowed(test["input"])

            assert result == test["expect"]

    def test_internalServerError(self):
        tests = [
            {
                "name": "single byte character",
                "case": "normal",
                "input": {"status": "Success"},
                "expect": {
                    "statusCode": 500,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "Success"}',
                },
            },
            {
                "name": "multi byte character",
                "case": "normal",
                "input": {"status": "成功"},
                "expect": {
                    "statusCode": 500,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": '{"status": "成功"}',
                },
            },
        ]

        for test in tests:
            result = Controller().internalServerError(test["input"])

            assert result == test["expect"]
