def lambda_handler(event, context):
    # TODO implement
    userId = event["params"]["path"]["userId"]
    if userId[0] == '"' and userId[-1] == '"':
        userId = userId[1:-1]
    return userId
