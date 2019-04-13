from libs.api_controller import Controller, validate
from libs.aws_resource_controller import dynamoController

schema = {"id": {"type": "string", "regex": "[0-9].*"}}


class GetIdController(Controller):
    @validate(schema)
    def handler(self, params):
        """
        Lambdaのメインハンドラから渡されたパラメータを受け取り、応答を返す
            :param self: インスタンス
            :param params: 辞書型(関数内の処理が実行される前にバリデーション処理が行われる)
        """
        reqid = params.get("id")
        res = dynamoController().searchId(reqid)

        if res.get("Count") == 0:
            return self.bad(
                {
                    "header": {
                        "status": "Error",
                        "errors": [{"field": "id", "message": "Unsupported coupon id"}],
                    }
                }
            )

        return self.ok(
            {
                "header": {"status": "Success", "errors": []},
                "response": {"coupons": [res.get("Items")[0]]},
            }
        )
