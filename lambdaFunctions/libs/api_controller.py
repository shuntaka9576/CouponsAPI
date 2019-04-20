import json

from cerberus import Validator


def _formatError(v):
    """
    エラーが複数ある場合、配列に詰め直す関数
    """
    error_messages = v.errors
    errors = []
    for e in v._errors:
        errors.append({"field": e.field, "message": error_messages.get(e.field)[0]})
        del error_messages.get(e.field)[0]
    return errors


def validate(schema):
    """
    Controllerに渡されるパラメータのバリデーションチェックを行うアノテーション
    """

    def _validate(func):
        def wrapper(*args, **kwargs):
            v = Validator(schema)
            if not v.validate(args[1]):
                return args[0].bad(
                    {"header": {"status": "Error", "errors": _formatError(v)}}
                )
            args = list(args)
            args[1] = v.document
            return func(*args, **kwargs)

        return wrapper

    return _validate


class Controller:
    """
    各APIは本Controllerを継承して作成する
    """

    def ok(self, body):
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"  # Required for CORS support to work
            },
            "body": json.dumps(body, ensure_ascii=False),
        }

    def bad(self, body):
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(body, ensure_ascii=False),
        }

    def methodNotAllowed(self, body):
        return {
            "statusCode": 405,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(body, ensure_ascii=False),
        }

    def internalServerError(self, body):
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(body, ensure_ascii=False),
        }
