import json
from couponsApi.getList.getList_controller import GetListController
from tests.fixture import initdb, couponTestDatas


class TestGetListController:
    def test_handler_200_successValue(self, initdb):
        input = {"path": "/coupons"}
        expectCode = 200
        expectRes = {
            "header": {
                "status": "Success",
                "errors": []
            },
            "response": {
                "coupons": couponTestDatas
            }
        }
        expectCode = 200
        want = GetListController().handler(input)
        wantBody = json.loads(want["body"])
        assert expectCode == want["statusCode"]
        assert expectRes == wantBody

    # validateが正しく動いているか確認
    def test_handler_400_failValue(self):
        expectCode = 400
        input = {"path": "/couponss"}
        want = GetListController().handler(input)

        assert expectCode == want["statusCode"]
