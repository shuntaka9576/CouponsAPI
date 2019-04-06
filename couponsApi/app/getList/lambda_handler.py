from app.getList.getList_controller import GetListController


def lambda_handler(event, context):
    print("recived event:", event)
    path = event.get("path")
    return GetListController().handler({"path": path})
