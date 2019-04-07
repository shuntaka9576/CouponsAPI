from libs.dynamo_controller import dynamoRepository
from libs.api_controller import validate
from libs.api_controller import Controller

schema = {
    "id": {
        "type": "string",
        'regex': '[0-9].*',
    }
}


class GetIdController(Controller):
    def __init__(self):
        self.dynamoRepo = dynamoRepository()

    @validate(schema)
    def handler(self, params):
        reqid = params['id']
        res = self.dynamoRepo.searchId(reqid)
        if res["Count"] == 0:
            return self.bad({
                "header": {
                    "status": "Error",
                    "errors": [{
                        "field": "id",
                        "message": "Unsupported coupon id"
                    }]
                },
            })

        return self.ok({
            "header": {
                "status": "Success",
                "errors": []
            },
            "response": {
                "coupons": [res["Items"][0]]
            }
        })
