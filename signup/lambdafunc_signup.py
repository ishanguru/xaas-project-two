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

botoconn = boto.sns.connect_to_region('us-east-1')

verificationconn = boto.ses.connect_to_region(
    'us-east-1',
    aws_access_key_id='AKIAIPCCURMQDHIB32HQ',
    aws_secret_access_key='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')


def lambda_handler(event, context):
    print("EVENT")
    print(str(event))
    if event and "userid" in event:
        user = connectdb.users.find_one({"_id": ObjectId(event["userid"])})
        if (not user) or ("name" not in user):
            return "error"
        dictToReturn = {}
        dictToReturn["name"] = str(user["name"])
        return dictToReturn

    users = db.users

    if ("Records" in event):
        event = event["Records"][0]["Sns"]["Message"]

    # event = json.loads(str(event))
    verifymail = {"username": "DONTSENDANEMAIL", "id": "DONTSENDANEMAIL"}

    existing_user = users.find_one({'_id': ObjectId(event["dbUserId"])})
    if existing_user:
        connectdb.users.update_one(
            {"_id": ObjectId(event["dbUserId"])},
            {'$set': {'status': 'unverified', 'name': event["username"], 'password': event["password"]}}
        )
        newuser = event['username']
        print(newuser)
        print('creating user for', event['username'])
        hashpass = event['password']
        verifymail = {"username": str(newuser), "id": id}
    return verifymail
