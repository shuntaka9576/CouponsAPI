from datetime import datetime
from libs.api_controller import validate
from libs.api_controller import Controller
from libs.aws_resource_controller import dynamoController

pathSchema = {
    "path": {
        "type": "string",
        'regex': "/coupons"
    }
}

querySchema = {
    "startdate": {
        "type": "string",
        'required': True,
        'regex': '[0-9]{8}'
    },
    "enddate": {
        "type": "string",
        'required': True,
        'regex': '[0-9]{8}'
    }
}


class GetListController(Controller):
    @validate(pathSchema)
    def pathHandler(self, params):
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

    @validate(querySchema)
    def queryHandler(self, params):
        res = dynamoController().scanAll()

        startDate = datetime.strptime(
            params.get("startdate"), "%Y%m%d")
        endDate = datetime.strptime(
            params.get("enddate"), "%Y%m%d")

        if startDate > endDate:
            return self.bad({
                "header": {
                    "status": "Error",
                    "errors": [{
                        "filed": "start-date",
                        "message": "period that does not exist"
                    }]
                }
            })

        rescoupons = []
        for coupon in res.get("Items"):
            couponStartDate = datetime.strptime(
                coupon.get("start-date"), "%Y%m%d")
            couponEndDate = datetime.strptime(
                coupon.get("end-date"), "%Y%m%d")
            print(startDate <= couponStartDate and endDate >= couponEndDate)
            if startDate <= couponStartDate and endDate >= couponEndDate:
                rescoupons.append(coupon)

        return self.ok({
            "header": {
                "status": "Success",
                "errors": []
            },
            "response": {
                "coupons": rescoupons
            }
        })
