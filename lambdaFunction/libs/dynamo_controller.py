import boto3
from boto3.dynamodb.conditions import Key
import os


class dynamoRepository:
    def __init__(self):
        if os.getenv("AWS_SAM_LOCAL"):
            dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url='http://localhost:4569'
            )
        else:
            dynamodb = boto3.resource('dynamodb')

        self.dynamodb = dynamodb
        self.table = 'coupons'

    def searchId(self, id):
        table = self.dynamodb.Table(self.table)
        res = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )
        return res

    def scanAll(self):
        table = self.dynamodb.Table(self.table)
        try:
            res = table.scan()
            return res
        except Exception as e:
            return e
