import os

import boto3
from boto3.dynamodb.conditions import Key


class dynamoController:
    def __init__(self, obj=None):
        if obj is None:
            if os.getenv("AWS_SAM_LOCAL"):
                self.dynamodb = boto3.resource(
                    "dynamodb", endpoint_url="http://localhost:4569/"
                )
            else:
                self.dynamodb = boto3.resource("dynamodb")
        else:
            self.dynamodb = obj
        self.table = self.dynamodb.Table("coupons")

    def searchId(self, id):
        try:
            return self.table.query(KeyConditionExpression=Key("id").eq(id))
        except Exception as e:
            print("dynamoController searchId() error:", e)
            raise e

    def scanAll(self):
        try:
            return self.table.scan()
        except Exception as e:
            print("dynamoController scanAll() error:", e)
            raise e

    def putItem(self, item):
        try:
            self.table.put_item(Item=item)
        except Exception as e:
            print("dynamoController putItem() error:", e)
            raise e


class s3Controller:
    def __init__(self, obj=None):
        if obj is None:
            if os.getenv("AWS_SAM_LOCAL"):
                self.s3 = boto3.client("s3", endpoint_url="http://localhost:4572/")
            else:
                self.s3 = boto3.client("s3")
        else:
            self.dynamodb = obj

    def getObject(self, bucket, key):
        try:
            return self.s3.get_object(Bucket=bucket, Key=key)
        except Exception as e:
            print("s3Controller getObject() error:", e)
            raise e
