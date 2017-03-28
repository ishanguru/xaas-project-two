import requests 
import boto3
import json

def lambda_handler(event, context):
    method = event["method"]
    if method == "login":
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName='microserviceQueue')
        queue.send_message(MessageBody=json.dumps(event))
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
