import boto3
import ConfigParser
import os
from boto3 import Session
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

config_file_path = os.environ['LAMBDA_TASK_ROOT'] + '/configurations.txt'

config = ConfigParser.ConfigParser()
config.readfp(open(config_file_path))

awsAccessKey = config.get('AWS Keys', 'awsAccessKeyId')
awsSecretKey = config.get('AWS Keys', 'awsSecretAccessKeyId')
awsRegion = config.get('AWS Keys', 'awsRegion')

aws_session = Session(
    aws_access_key_id=awsAccessKey,
    aws_secret_access_key=awsSecretKey,
    region_name=awsRegion,
)

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]

try:
    sqs_queue = aws_session.client('sqs')
except Exception as e:
    print("Queue already exists")


def payments_handler(event, context):
    current_caid = event['orderid']
    result = payments(current_caid)
    return result


def getDictWithUserInfo(paymentObj):
    user = connectdb.users.find_one({"name": str(paymentObj["user_email"])})

    userDict = {}
    toReturn = {}
    toReturn["data"] = paymentObj

    selfLink = {}
    selfLink["type"] = "self"
    selfLink["href"] = "/orders/" + str(paymentObj["_id"])

    userLink = {}
    userLink["type"] = "user"
    userLink["href"] = "/users/" + str(user["_id"])

    toReturn["links"] = [selfLink, userLink]

    return toReturn


def payments(current_caid):
    queue_url = sqs_queue.get_queue_url(QueueName='ordersQueue')
    messages = sqs_queue.receive_message(QueueUrl=queue_url['QueueUrl'])
    print
    len(messages['Messages']), messages['Messages']
    for item in messages['Messages']:
        # 		caid = message.message_attributes.get('caid').get('StringValue')
        caid = item['Body']
        caid = json.loads(caid)
        print
        "item", caid['_id']
        print
        "us", current_caid
        if caid['_id'] == current_caid:
            body = item['Body']
            print
            body
            sqs_queue.delete_message(QueueUrl=queue_url['QueueUrl'], ReceiptHandle=item['ReceiptHandle'])
            return getDictWithUserInfo(body)

    paymentObject = connectdb.orders.find_one({"_id": ObjectId(str(current_caid))})

    if paymentObject:
        paymentObject["_id"] = str(current_caid)
        return getDictWithUserInfo(paymentObject)

    raise Exception({"Not_Found": "Item not found"})