def lambda_handler(event, context):
    method = event["method"]
    if method == "login":
        return "login"
    elif method == "logout":
        return "logout"
    elif method == "signUp":
        return "sign up"
    elif method == "charge":
        return "charge"
    else:
        return "not supported"
    return str(event)