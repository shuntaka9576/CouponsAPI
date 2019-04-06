from libs.dynamo_controller import dynamoRepository
from libs.api_controller import validate
from libs.api_controller import Controller

schema = {
    "path": {
        "type": "string",
        "regex": "/coupons",
    }
}


class GetListController(Controller):
    def __init__(self):
        self.dynamoRepo = dynamoRepository()

    @validate(schema)
    def handler(self, params):
        res = self.dynamoRepo.scanAll()
        return self.ok({
            "header": {
                "status": "Success",
                "errors": []
            },
            "response": {
                "coupons": [res["Items"]]
            }
        })
