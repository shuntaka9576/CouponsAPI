import json
import sys

from couponsApi.getId.getId_controller import GetIdController


def lambda_handler(event, context):
    """
    GET,POST /coupons/{id} 問い合わせ時に、最初に呼び出される関数
        :param event: Lambdaに渡されるイベント情報
        :param context: Lambdaに渡されるライタイム情報
    """
    print("recived event:", event)

    if event.get("httpMethod") == "GET":
        params = event.get("pathParameters")
    elif event.get("httpMethod") == "POST":
        params = event.get("body")
        if event.get("body") is not None:
            try:
                params = json.loads(event.get("body"))
            except Exception as e:
                print("POST body Message parse error:", e)
                return GetIdController().bad(
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
            return GetIdController().bad(
                {
                    "header": {
                        "status": "Error",
                        "errors": [
                            {"filed": "POST Body", "message": "POST body empty"}
                        ],
                    }
                }
            )
    else:
        print("Unexpected HTTP method has been triggered:", event.get("httpMethod"))
        sys.exit(1)

    return GetIdController().handler(params)
