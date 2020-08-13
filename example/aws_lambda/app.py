from xmlabs.aws_lambda import lambda_handler

@lambda_handler
def main(event, context, config):
    print(config.STRIPE_API_SECRET_KEY)
    pass

if __name__ == "__main__":
    main({"headers":{"X-Environment": "dev"}}, {})
    main({"headers":{"X-Environment": "prod"}}, {})
    main({"headers":{"X-Environment": "dev"}}, {})
    main({"headers":{"X-Environment": "dev"}}, {})
    main({"headers":{"X-Environment": "prod"}}, {})


