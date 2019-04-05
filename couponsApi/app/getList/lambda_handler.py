from app.libs.dynamo_controller import dynamoRepository
from app.libs.api_controller import validate
from app.libs.api_controller import Controller


class GetListController(Controller):
    def __init__(self):
        self.dynamoRepo = dynamoRepository()

    @validate(schema)
    def handler(self, params):
        reqid = params['id']
        res = self.dynamoRepo.searchId(reqid)
        # TODO Countが1以外の時のエラーハンドリング処理

        return self.ok({
            "header": {
                "status": "Success",
                "errors": []
            },
            "response": {
                "coupons": [res["Items"]]
            }
        })
