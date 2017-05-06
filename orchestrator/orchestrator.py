from pymongo import MongoClient
import boto3
import json
import jwt


def lambda_handler(event, context):
    # if 'context' in event:
    #     print("hey")
    # else:
    #     return "YOURE DOING SOMETHING WRONG!"
    print ("THIS IS THE EVENT!")
    print (event)
    print("THESE ARE THE KEYS")
    print(event.keys())
    print("THESE ARE THE CONTEXT KEYS")
    print(event['context'].keys())
    print("THIS IS THE resource-path")
    print(event['context']['resource-path'])



    method = event['context']['resource-path']
    sns_client = boto3.client('sns')
    if method == "/login":
        connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
        aid = str(connectdb.loginAttempts.insert_one({"status" : "undefined"}).inserted_id);
        event["aid"] = aid
        event["body-json"]["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:login', Message=str(json.dumps(event["body-json"])))
        return aid
    elif method == "signup":
        client = boto3.client('stepfunctions')
        connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
        aid = str(connectdb.signupAttempts.insert_one({"status": "undefined"}).inserted_id);
        event["aid"] = aid
        response = client.start_execution(
            stateMachineArn='arn:aws:states:us-east-1:648812771825:stateMachine:HelloWorld098098',
            name=aid,
            input=str(json.dumps(event))
        )
        return aid
    elif method == "charge":
        encoded = event["jwt"]
        decoded = jwt.decode(encoded, 'secret', algorithms=['HS256'])
        email = decoded["email"]
        password = decoded["password"]
        user_db = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
        # users = user_db.users
        print("EMAIL")
        print(email)
        user = user_db.users.find_one({"name": email})
        if (user["password"] == password):
            chargeDb = MongoClient('mongodb://user1:user1password@ds149030.mlab.com:49030/charge_db')["charge_db"]
            aid = str(chargeDb.caids.insert_one({"status": "undefined"}).inserted_id);
            event["aid"] = aid
            response = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:648812771825:payments',
                Message=str(json.dumps(event)))
            return aid
        return "failure"
    else:
        # return event
        return "not supported"
    return str(event)
