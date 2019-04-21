from libs.api_controller import Controller, validate
from libs.aws_resource_controller import dynamoController
from libs.datetimeUtil import checkDate

pathSchema = {"path": {"type": "string", "regex": "/coupons"}}

querySchema = {
    "startdate": {"type": "string", "required": True, "regex": "[0-9]{8}"},
    "enddate": {"type": "string", "required": True, "regex": "[0-9]{8}"},
}


class GetListController(Controller):
    @validate(pathSchema)
    def pathHandler(self, params, obj=None):
        """
        Lambdaのメインハンドラから渡されたパラメータを受け取り、応答を返す
        クエリパラーメータが設定されていない場合、本関数が呼び出される
            :param self: インスタンス
            :param params: 辞書型(関数内の処理が実行される前にバリデーション処理が行われる)
        """
        try:
            print("List問い合わせ")
            if obj is None:
                res = dynamoController().scanAll()
            else:
                res = dynamoController(obj).scanAll()
        except Exception as e:
            print("pathHandler unexpected error: ", e)
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
                "response": {"coupons": res.get("Items")},
            }
        )

    @validate(querySchema)
    def queryHandler(self, params, obj=None):
        """
        Lambdaのメインハンドラから渡されたパラメータを受け取り、応答を返す
        クエリパラーメータが設定された場合、本関数が呼び出される
            :param self: インスタンス
            :param params: 辞書型(関数内の処理が実行される前にバリデーション処理が行われる)
        """
        try:
            print("List問い合わせ(期間付き)")
            if obj is None:
                res = dynamoController().scanAll()
            else:
                res = dynamoController(obj=obj).scanAll()

            errors = []
            startDate = checkDate(params.get("startdate"))
            endDate = checkDate(params.get("enddate"))
            if startDate is None:
                errors.append({"filed": "startdate", "message": "incorrect as date"})
            if endDate is None:
                errors.append({"filed": "enddate", "message": "incorrect as date"})
            if len(errors) > 0:
                return self.bad({"header": {"status": "Error", "errors": errors}})

            if startDate > endDate:
                return self.bad(
                    {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "filed": "startdate",
                                    "message": "startdate later than enddate",
                                }
                            ],
                        }
                    }
                )

            rescoupons = []
            for coupon in res.get("Items"):
                couponStartDate = checkDate(coupon.get("start-date"))
                couponEndDate = checkDate(coupon.get("end-date"))
                if startDate >= couponStartDate and endDate <= couponEndDate:
                    rescoupons.append(coupon)
            return self.ok(
                {
                    "header": {"status": "Success", "errors": []},
                    "response": {"coupons": rescoupons},
                }
            )
        except Exception as e:
            print("queryHandler unexpected error: ", e)
            return self.internalServerError(
                {
                    "header": {
                        "status": "Error",
                        "errors": [{"message": "Intenal server error"}],
                    }
                }
            )
