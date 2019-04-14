import json
import sys

from couponsApi.getList.getList_controller import GetListController


def lambda_handler(event, context):
    """
    GET,POST /coupons 問い合わせ時に、最初に呼び出される関数
        :param event: Lambdaに渡されるイベント情報
        :param context: Lambdaに渡されるライタイム情報
    """
    print("recived event:", event)

    if event.get("httpMethod") == "GET":
        path = event.get("path")
        query = event.get("queryStringParameters")
    elif event.get("httpMethod") == "POST":
        path = event.get("path")
        if event.get("body") is not None:
            try:
                query = json.loads(event.get("body"))
            except Exception as e:
                print("POST body Message parse error:", e)
                return GetListController().bad(
                    {
                        "header": {
                            "status": "Error",
                            "errors": [
                                {
                                    "filed": "POST Body",
                                    "message": "POST body parse error",
                                }
                            ],
                        }
                    }
                )
        else:
            query = None
    else:
        print("Unexpected HTTP method has been triggered:", event.get("httpMethod"))
        return GetListController().methodNotAllowed(
            {
                "header": {
                    "status": "Error",
                    "errors": [{"message": "Unsupported method"}],
                }
            }
        )

    if query is None:
        return GetListController().pathHandler({"path": path})
    else:
        return GetListController().queryHandler(query)
