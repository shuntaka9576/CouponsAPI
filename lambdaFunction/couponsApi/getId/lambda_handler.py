from getId.getId_controller import GetIdController


def lambda_handler(event, context):
    print("recived event:", event)
    params = event['pathParameters']
    return GetIdController().handler(params)
