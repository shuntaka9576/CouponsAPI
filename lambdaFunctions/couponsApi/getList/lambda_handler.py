from couponsApi.getList.getList_controller import GetListController


def lambda_handler(event, context):
    """
    coupons 問い合わせ時に、最初に呼び出される関数
        :param event: Lambdaに渡されるイベント情報
        :param context: Lambdaに渡されるライタイム情報
    """
    print("recived event:", event)
    path = event.get("path")
    query = event.get("queryStringParameters")

    if query is not None:
        return GetListController().queryHandler(query)
    else:
        return GetListController().pathHandler({"path": path})
