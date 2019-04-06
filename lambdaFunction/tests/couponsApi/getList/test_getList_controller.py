from couponsApi.getList.getList_controller import GetListController


class TestGetListController:
    def test_handler_200_SuccessValue(self):
        expectCode = 200
        input = {"path": "/coupons"}
        want = GetListController().handler(input)

        assert expectCode == want["statusCode"]

    # validateが正しく動いているか確認
    def test_handler_400_FailValue(self):
        expectCode = 400
        input = {"path": "/couponss"}
        want = GetListController().handler(input)

        assert expectCode == want["statusCode"]
