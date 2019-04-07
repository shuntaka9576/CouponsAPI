from libs.api_controller import validate
from libs.api_controller import Controller
from libs.aws_resource_controller import dynamoController

schema = {
    "path": {
        "type": "string",
        "regex": "/coupons",
    }
}


class GetListController(Controller):
    @validate(schema)
    def handler(self, params):
        res = dynamoController().scanAll()
        return self.ok({
            "header": {
                "status": "Success",
                "errors": []
            },
            "response": {
                "coupons": res["Items"]
            }
        })
