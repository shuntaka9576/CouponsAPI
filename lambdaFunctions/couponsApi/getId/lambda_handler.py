from couponsApi.getId.getId_controller import GetIdController


def lambda_handler(event, context):
    """
    GET /coupons/{id} 問い合わせ時に、最初に呼び出される関数
        :param event: Lambdaに渡されるイベント情報
        :param context: Lambdaに渡されるライタイム情報
    """
    print("recived event:", event)

    if event.get("httpMethod") == "GET":
        params = event.get("pathParameters")
    else:
        print("Unexpected HTTP method has been triggered:", event.get("httpMethod"))
        return GetIdController().methodNotAllowed(
            {
                "header": {
                    "status": "Error",
                    "errors": [{"message": "Unsupported method"}],
                }
            }
        )

    return GetIdController().handler(params)
