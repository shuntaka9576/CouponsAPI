from couponsApi.getId.getId_controller import GetIdController


class TestGetIdController:
    def test_handler_200_SuccessValue(self):
        input = {"id": "0001245"}
        expectCode = 200
        want = GetIdController().handler(input)
        assert expectCode == want["statusCode"]

    def test_handler_400_IntegerValue(self):
        expectCode = 400
        input = {"id": 1245}
        want = GetIdController().handler(input)
        assert expectCode == want["statusCode"]

    def test_handler_400_NotNumberValue(self):
        input = {"id": "zeroonetwo"}
        expectCode = 400
        want = GetIdController().handler(input)
        assert expectCode == want["statusCode"]

    def test_handler_400_UnsupportedCouponId(self):
        input = {"id": "000111"}
        expectCode = 400
        want = GetIdController().handler(input)
        assert expectCode == want["statusCode"]
