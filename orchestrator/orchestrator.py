from pymongo import MongoClient
import boto3
import json


def lambda_handler(event, context):
    method = event["method"]
    sns_client = boto3.client('sns')
    if method == "login":
        connectdb = MongoClient('mongodb://user1:password@ds149040.mlab.com:49040/user_db')
        aid = connectdb.loginAttempts.insert({"status" : "undefined"});
        event["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:login', Message=json.dumps(event))
        return aid
    elif method == "signup":
        connectdb = MongoClient('mongodb://user1:password@ds149040.mlab.com:49040/user_db')
        aid = connectdb.signupAttempts.insert({"status": "undefined"});
        event["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:signup', Message=json.dumps(event))
        return aid
    elif method == "charge":
        connectdb = MongoClient('mongodb://user1:password@ds149030.mlab.com:49030/charge_db')
        aid = connectdb.caids.insert({"status": "undefined"});
        event["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:payments', Message=json.dumps(event))
        return aid
    else:
        return "not supported"
    return str(event)
