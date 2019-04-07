import json
import termcolor
from couponsApi.getId.getId_controller import GetIdController
from tests.fixture import initdb, couponTestDatas


class TestGetIdController:
    def test_handler_200_successValue1(self, initdb):
        for coupon in couponTestDatas:
            input = {"id": coupon["id"]}
            expectCode = 200
            expectRes = {
                "header": {
                    "status": "Success",
                    "errors": []
                },
                "response": {
                    "coupons": [coupon]
                }
            }

            want = GetIdController().handler(input)
            # 文字列だと比較出来ないので、辞書型にキャストして比較
            wantBody = json.loads(want["body"])
            assert expectCode == want["statusCode"]
            assert expectRes == wantBody

    def test_handler_400_integerValue(self, initdb):
        expectCode = 400
        input = {"id": 1245}
        want = GetIdController().handler(input)
        assert expectCode == want["statusCode"]

    def test_handler_400_notNumberValue(self, initdb):
        input = {"id": "zeroonetwo"}
        expectCode = 400
        want = GetIdController().handler(input)
        assert expectCode == want["statusCode"]

    def test_handler_400_unsupportedCouponId(self, initdb):
        input = {"id": "000111"}
        expectCode = 400
        want = GetIdController().handler(input)
        assert expectCode == want["statusCode"]
