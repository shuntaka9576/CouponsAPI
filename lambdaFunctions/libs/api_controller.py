import json
from cerberus import Validator


def _formatError(v):
    error_messages = v.errors
    errors = []
    for e in v._errors:
        errors.append({
            "field": e.field,
            "message": error_messages[e.field][0]
        })
        del error_messages[e.field][0]
    return errors


def validate(schema):
    def _validate(func):
        def wrapper(*args, **kwargs):
            v = Validator(schema)
            if not v.validate(args[1]):
                return args[0].bad({
                    "header": {
                        "status": "Error",
                        "errors": _formatError(v)
                    }
                })
            args = list(args)
            args[1] = v.document
            return func(*args, **kwargs)
        return wrapper
    return _validate


class Controller:
    def ok(self, body):
        return {
            "statusCode": 200,
            "body": json.dumps(body, ensure_ascii=False),
        }

    def bad(self, body):
        return {
            "statusCode": 400,
            "body": json.dumps(body, ensure_ascii=False),
        }

    def notfound(self, body):
        return {
            "statusCode": 404,
            "body": json.dumps(body, ensure_ascii=False),
        }
