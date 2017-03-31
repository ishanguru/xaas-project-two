from pymongo import MongoClient
import boto3
import json


def lambda_handler(event, context):
    method = event["method"]
    sns_client = boto3.client('sns')
    if method == "login":
        connectdb = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
        laid = connectdb.loginAttempts.insert({"status" : "undefined"});
        event["laid"] = laid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:login', Message=json.dumps(event))
        return laid
    elif method == "signup":
        connectdb = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
        said = connectdb.signupAttempts.insert({"status": "undefined"});
        event["said"] = said
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:signup', Message=json.dumps(event))
        return said
    elif method == "charge":
        connectdb = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/chargedb')
        caid = connectdb.signupAttempts.insert({"status": "undefined"});
        event["caid"] = caid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:payments', Message=json.dumps(event))
        return caid
    else:
        return "not supported"
    return str(event)
