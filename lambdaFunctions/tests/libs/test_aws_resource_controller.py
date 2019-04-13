import boto3
import pytest
from botocore.config import Config
from tests.fixture import couponTestDatas, initDb, initS3

from libs.aws_resource_controller import dynamoController, s3Controller


class TestDynamoController:
    def test_searchId_success(self, initDb):
        tests = [
            {
                "name": "valid value",
                "case": "normal",
                "input": "0001245",
                "expect": [couponTestDatas["0001245"]],
            }
        ]

        for test in tests:
            record = dynamoController().searchId(test["input"])

            assert record["Items"] == test["expect"]

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

            assert record["Items"] == test["expect"]

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
                "input": couponTestDatas["0001245"],
                "expect": {"Items": couponTestDatas["0001245"], "Count": 1},
            }
        ]

        for test in tests:
            dynamoController().putItem(test["input"])
            result = dynamoController().scanAll()

            assert result["Items"][0] == test["expect"]["Items"]
            assert result["Count"] == test["expect"]["Count"]

    def test_putItem_connectionFail(self):
        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://localhost:9999/", config=config
        )
        with pytest.raises(Exception):
            dynamoController(obj=dynamodb).putItem(couponTestDatas["0001245"])


class TestS3Controller:
    def test_s3putItem_connectionFail(self, initS3):
        config = Config(connect_timeout=1, read_timeout=1, retries=dict(max_attempts=1))
        s3 = boto3.client("s3", endpoint_url="http://localhost:9999/", config=config)
        with pytest.raises(Exception):
            s3Controller(obj=s3).getObject(
                "dev-cpa-s3-coupons", "dynamo/initDbData.json"
            )
