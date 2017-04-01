from pymongo import MongoClient
import boto3
import json


def lambda_handler(event, context):
    method = event["method"]
    sns_client = boto3.client('sns')
    if method == "login":
        connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
        aid = str(connectdb.loginAttempts.insert_one({"status" : "undefined"}).inserted_id);
        event["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:login', Message=str(json.dumps(event)))
        return aid
    elif method == "signup":
        connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
        aid = str(connectdb.signupAttempts.insert_one({"status": "undefined"}).inserted_id);
        event["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:signup', Message=str(json.dumps(event)))
        return aid
    elif method == "charge":
        connectdb = MongoClient('mongodb://user1:user1password@ds149030.mlab.com:49030/charge_db')["charge_db"]
        aid = str(connectdb.caids.insert_one({"status": "undefined"}).inserted_id);
        event["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:payments', Message=str(json.dumps(event)))
        return aid
    else:
        return "not supported"
    return str(event)
