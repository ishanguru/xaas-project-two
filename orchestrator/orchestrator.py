import requests 
import boto3
import json


def lambda_handler(event, context):
    method = event["method"]
    if method == "login":
    	sns_client = boto3.client('sns')
    	response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:accounts', Message=json.dumps(event))
        return "login"
    elif method == "signUp":
    	sns_client = boto3.client('sns')
    	response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:accounts', Message=json.dumps(event))
        return "sign up"
    elif method == "charge":
    	sns_client = boto3.client('sns')
    	response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:payments', Message=json.dumps(event))
        return "charge"
    else:
        return "not supported"
    return str(event)
