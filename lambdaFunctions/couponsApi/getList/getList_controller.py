from datetime import datetime

from libs.api_controller import Controller, validate
from libs.aws_resource_controller import dynamoController

pathSchema = {"path": {"type": "string", "regex": "/coupons"}}

querySchema = {
    "startdate": {"type": "string", "required": True, "regex": "[0-9]{8}"},
    "enddate": {"type": "string", "required": True, "regex": "[0-9]{8}"},
}


class GetListController(Controller):
    @validate(pathSchema)
    def pathHandler(self, params):
        """
        Lambdaのメインハンドラから渡されたパラメータを受け取り、応答を返す
        クエリパラーメータが設定されていない場合、本関数が呼び出される
            :param self: インスタンス
            :param params: 辞書型(関数内の処理が実行される前にバリデーション処理が行われる)
        """

        print("List問い合わせ")
        res = dynamoController().scanAll()
        return self.ok(
            {
                "header": {"status": "Success", "errors": []},
                "response": {"coupons": res.get("Items")},
            }
        )

    @validate(querySchema)
    def queryHandler(self, params):
        """
        Lambdaのメインハンドラから渡されたパラメータを受け取り、応答を返す
        クエリパラーメータが設定された場合、本関数が呼び出される
            :param self: インスタンス
            :param params: 辞書型(関数内の処理が実行される前にバリデーション処理が行われる)
        """

        print("List問い合わせ(期間付き)")
        res = dynamoController().scanAll()

        startDate = datetime.strptime(params.get("startdate"), "%Y%m%d")
        endDate = datetime.strptime(params.get("enddate"), "%Y%m%d")

        if startDate > endDate:
            return self.bad(
                {
                    "header": {
                        "status": "Error",
                        "errors": [
                            {
                                "filed": "start-date",
                                "message": "period that does not exist",
                            }
                        ],
                    }
                }
            )

        rescoupons = []
        for coupon in res.get("Items"):
            couponStartDate = datetime.strptime(coupon.get("start-date"), "%Y%m%d")
            couponEndDate = datetime.strptime(coupon.get("end-date"), "%Y%m%d")
            if startDate >= couponStartDate and endDate <= couponEndDate:
                rescoupons.append(coupon)

        return self.ok(
            {
                "header": {"status": "Success", "errors": []},
                "response": {"coupons": rescoupons},
            }
        )
