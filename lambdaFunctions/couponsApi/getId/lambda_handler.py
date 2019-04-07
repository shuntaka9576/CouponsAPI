from couponsApi.getId.getId_controller import GetIdController


def lambda_handler(event, context):
    """
    coupons/{id} 問い合わせ時に、最初に呼び出される関数
        :param event: Lambdaに渡されるイベント情報
        :param context: Lambdaに渡されるライタイム情報
    """
    print("recived event:", event)
    params = event.get("pathParameters")
    return GetIdController().handler(params)
