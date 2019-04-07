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
        GET /coupons 問い合わせ応答処理
        Lambdaから渡されたパラメータを受け取り、全てのクーポン一覧を返却
            :param self: インスタンス
            :param params: 辞書型
        """

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
        GET /coupons?startdate=yyyymmdd&enddate=yyyymmdd 問い合わせ処理
        Lambdaから渡されたパラメータを受け取り、指定された期間永続的に利用可能なクーポン一覧を返却
            :param self: インスタンス
            :param params: 辞書型
        """
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
