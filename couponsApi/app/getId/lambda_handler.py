from app.getId.getId_controller import GetIdController


def lambda_handler(event, context):
    params = event['pathParameters']
    return GetIdController().handler(params)
