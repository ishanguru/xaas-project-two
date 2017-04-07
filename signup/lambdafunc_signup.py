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

verificationconn = boto.ses.connect_to_region(
        'us-east-1',
        aws_access_key_id='AKIAIPCCURMQDHIB32HQ',
        aws_secret_access_key='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')


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
        verificationconn.send_email(
        'nachi.2605@gmail.com',
        'Verify your email',
        'Enter the Lambda function here',
        [event['username']])
        return " Successful Registration"
