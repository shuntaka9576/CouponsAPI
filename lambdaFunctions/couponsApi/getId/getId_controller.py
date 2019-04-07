from libs.api_controller import validate
from libs.api_controller import Controller
from libs.aws_resource_controller import dynamoController

schema = {
    "id": {
        "type": "string",
        'regex': '[0-9].*',
    }
}


class GetIdController(Controller):
    @validate(schema)
    def handler(self, params):
        reqid = params['id']
        res = dynamoController().searchId(reqid)

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
