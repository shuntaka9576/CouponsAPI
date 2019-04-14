from libs.api_controller import Controller, validate
from libs.aws_resource_controller import dynamoController

schema = {"id": {"type": "string", "regex": "[0-9].*"}}


class GetIdController(Controller):
    @validate(schema)
    def handler(self, params, obj=None):
        """
        Lambdaのメインハンドラから渡されたパラメータを受け取り、応答を返す
            :param self: インスタンス
            :param params: 辞書型(関数内の処理が実行される前にバリデーション処理が行われる)
        """
        try:
            reqid = params.get("id")
            if obj is None:
                res = dynamoController().searchId(reqid)
            else:
                res = dynamoController(obj).searchId(reqid)

            if res.get("Count") == 0:
                return self.bad(
                    {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {"field": "id", "message": "Unsupported coupon id"}
                            ],
                        }
                    }
                )
        except Exception as e:
            print("GetIdController unexpected error: ", e)
            return self.internalServerError(
                {
                    "header": {
                        "status": "Error",
                        "errors": [{"message": "Intenal server error"}],
                    }
                }
            )

        return self.ok(
            {
                "header": {"status": "Success", "errors": []},
                "response": {"coupons": [res.get("Items")[0]]},
            }
        )
