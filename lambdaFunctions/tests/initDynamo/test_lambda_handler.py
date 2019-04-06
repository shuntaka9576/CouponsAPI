def test_lambda_handler():
    from initDynamo.lambda_handler import lambda_handler
    input = {"Records": [{
        's3': {
            "bucket": {
                "name": "dev-cpa-s3-coupons",
            },
            "object": {
                "key": "dynamodb/initDbData.json",
            }
        }
    }
    ]}

    lambda_handler(input, {})
