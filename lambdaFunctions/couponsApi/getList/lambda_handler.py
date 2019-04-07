from couponsApi.getList.getList_controller import GetListController


def lambda_handler(event, context):
    print("recived event:", event)
    path = event.get("path")
    query = event.get("queryStringParameters")

    if query is not None:
        return GetListController().queryHandler(
            query
        )
    else:
        return GetListController().pathHandler({
            "path": path
        })
