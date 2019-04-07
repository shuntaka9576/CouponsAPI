import boto3
import pytest
from botocore.config import Config
from tests.fixture import couponTestDatas, initDb

from libs.aws_resource_controller import dynamoController


class TestDynamoController:
    def test_searchId_success(self, initDb):
        tests = [
            {
                "name": "valid value",
                "case": "normal",
                "input": "0001245",
                "expect": [couponTestDatas.get("0001245")],
            }
        ]

        for test in tests:
            record = dynamoController().searchId(test.get("input"))

            assert record.get("Items") == test.get("expect")

    def test_searchId_connectionFail(self, initDb):
        """ DBのエンドポイント接続不可テスト
        指定した宛先は、LISTENしていないポートを指定
        """

        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://localhost:9999/", config=config
        )
        with pytest.raises(Exception):
            dynamoController(obj=dynamodb).searchId("0001245")

    def test_scanAll_success(self, initDb):
        testDatas = [couponTestDatas[couponKey] for couponKey in couponTestDatas]
        tests = [{"name": "valid value", "case": "normal", "expect": testDatas}]

        for test in tests:
            record = dynamoController().scanAll()

            assert record.get("Items") == test.get("expect")

    def test_scanAll_connectionFail(self, initDb):
        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://localhost:9999/", config=config
        )
        with pytest.raises(Exception):
            dynamoController(obj=dynamodb).scanAll()

    def test_putItem_success(self):
        tests = [
            {
                "name": "valid value",
                "input": couponTestDatas.get("0001245"),
                "expect": {"Items": couponTestDatas.get("0001245"), "Count": 1},
            }
        ]

        for test in tests:
            dynamoController().putItem(test.get("input"))
            result = dynamoController().scanAll()

            assert result.get("Items")[0] == test.get("expect").get("Items")
            assert result.get("Count") == test.get("expect").get("Count")

    def test_putItem_connectionFail(self):
        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://localhost:9999/", config=config
        )
        with pytest.raises(Exception):
            dynamoController(obj=dynamodb).putItem(couponTestDatas.get("0001245"))
