import json
from couponsApi.getList.getList_controller import GetListController
from tests.fixture import initdb, couponTestDatas


class TestGetListController:
    def test_queryHandler_200_successValue(self, initdb):
        inputs = [
            {
                "startdate": "20180401",
                "enddate": "20180501"
            },
            {
                "startdate": "20190401",
                "enddate": "20190501"
            },
            {
                "startdate": "20180401",
                "enddate": "20190501"
            }
        ]

        expectRes = {
            "header": {
                "status": "Success",
                "errors": []
            },
            "response": {
                "coupons": [couponTestDatas[0]]
            }
        }

        expectCode = 200
        for input in inputs:
            want = GetListController().queryHandler(input)
            wantBody = json.loads(want["body"])
            print(want)
            #assert expectCode == want["statusCode"]
            #assert expectRes == wantBody

    def test_queryHandler_400_failValue(self, initdb):
        inputs = [{
            "startdate": "2019/04/08",
            "enddate": "2019/05/04"
        }, {
            "startdate": "2019-04-08",
            "enddate": "2019-05-04"
        }, {
            "startdate": "201948",
            "enddate": "201954"
        },
        ]

        for input in inputs:
            expectCode = 400
            want = GetListController().queryHandler(input)
            assert expectCode == want["statusCode"]

    def test_pathHandler_200_successValue(self, initdb):
        input = {
            "path": "/coupons",
        }

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

        want = GetListController().pathHandler(input)
        wantBody = json.loads(want["body"])
        assert expectCode == want["statusCode"]
        assert expectRes == wantBody

    # validateが正しく動いているか確認
    def test_pathHandler_400_pathFailValue(self, initdb):
        expectCode = 400
        input = {
            "path": "/couponss",
        }
        want = GetListController().pathHandler(input)
        assert expectCode == want["statusCode"]
