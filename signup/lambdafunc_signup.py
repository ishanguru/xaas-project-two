from pymongo import MongoClient
import boto.sns
import boto.ses
import boto.sqs
from boto.sqs.message import RawMessage
from bson.objectid import ObjectId
import json

## Connection with the MongoDB
connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb


botoconn = boto.sns.connect_to_region( 'us-east-1' )

# verificationconn = boto.ses.connect_to_region(
#         'us-east-1',
#         aws_access_key_id='AKIAJN3ACGV3J6SG3Q5A',
#         aws_secret_access_key='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')

## Set up existing AWS SQS
# conf = { "sqs-access-key": "AKIAJN3ACGV3J6SG3Q5A",
# "sqs-secret-key": "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",
# "sqs-queue-name": "queue_signup",
# "sqs-region": "us-east-1",
# "sqs-path": "sqssend"
#
# }
#
# conn = boto.sqs.connect_to_region(
#         conf.get('sqs-region'),
#         aws_access_key_id   = conf.get('sqs-access-key'),
#         aws_secret_access_key   = conf.get('sqs-secret-key')
# )
#
# q = conn.get_queue('queue_signup')


def lambda_handler(event, context):
    print ("EVENT")
    print (str(event))
    if "type" in event and event["type"] == "signupQuery":
        matchingAttempt = connectdb.signupAttempts.find_one({"_id": ObjectId(event["aid"])})
        print(type(matchingAttempt))
        dictToReturn = {}
        dictToReturn["status"] = str(matchingAttempt["status"])
        dictToReturn["aid"] = str(matchingAttempt["_id"])
        return dictToReturn

    users = db.users

    if ("Records" in event):
        event = event["Records"][0]["Sns"]["Message"]

    event = json.loads(str(event))

    existing_user = users.find_one({'name' : event["username"]})
    if existing_user:
        connectdb.signupAttempts.find_one_and_replace(
            {"_id": ObjectId(event["aid"])},
            {"status": "error"}
        )
        return 'That inputEmail already exists!'
    else:
        print('creating user for', event['username'] )
        hashpass = event['password']
        users.insert({'name' : event['username'], 'password' : hashpass})
        # verificationconn.verify_email_address(event['username'])
        connectdb.signupAttempts.find_one_and_replace(
            {"_id": ObjectId(event["aid"])},
            {"status": "success"}
        )
        return " Successful Registration"
