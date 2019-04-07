import boto3
from boto3.dynamodb.conditions import Key
import os


class awsResourceBase:
    def __init__(self):
        if os.getenv("AWS_SAM_LOCAL"):
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url='http://localhost:4569/'
            )
            self.s3 = boto3.client(
                's3',
                endpoint_url='http://localhost:4572/'
            )
        else:
            self.dynamodb = boto3.resource('dynamodb')
            self.s3 = boto3.client('s3')


class dynamoController(awsResourceBase):
    def __init__(self):
        super().__init__()
        self.table = self.dynamodb.Table('coupons')

    def searchId(self, id):
        try:
            return self.table.query(
                KeyConditionExpression=Key('id').eq(id)
            )
        except Exception as e:
            return e

    def scanAll(self):
        try:
            return self.table.scan()
        except Exception as e:
            return e

    def putItem(self, item):
        try:
            self.table.put_item(
                Item=item
            )
        except Exception as e:
            return e


class s3Controller(awsResourceBase):
    def __init__(self):
        super().__init__()
