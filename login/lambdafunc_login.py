from pymongo import MongoClient
import boto.sqs
from boto.sqs.message import RawMessage
from bson.objectid import ObjectId
import boto.ses
import boto.sns
import json

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb

conf = {"sqs-access-key": "AKIAJN3ACGV3J6SG3Q5A",
        "sqs-secret-key": "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",
        "sqs-queue-name": "queue_login",
        "sqs-region": "us-east-1",
        "sqs-path": "sqssend"

        }

conn = boto.sqs.connect_to_region(
    conf.get('sqs-region'),
    aws_access_key_id=conf.get('sqs-access-key'),
    aws_secret_access_key=conf.get('sqs-secret-key')
)

q = conn.get_queue('queue_login')

verificationconn = boto.ses.connect_to_region(
    'us-east-1',
    aws_access_key_id='AKIAIYILDTN5HSKGIAOA',
    aws_secret_access_key='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')

verifiedemails = verificationconn.list_verified_email_addresses()


def lambda_handler(event, context):

    #if polling
    if "type" in event and event["type"] == "loginQuery":
        matchingAttempt = connectdb.loginAttempts.find_one({"_id": ObjectId(event["aid"])})
        return str(matchingAttempt)

    users = db.users
    print("EVENT ORG")
    print(event)

    if ("Records" in event):
        event = event["Records"][0]["Sns"]["Message"]
    print ("EVENT")
    print (event)
    event = json.loads(str(event))
    print (type(event))
    login_user = users.find_one({'name': event['username']})


    if login_user:
        if event['username'] == login_user['name']:
            if event['password'] == login_user['password']:
                for a in verifiedemails.values():
                    for b in a.values():
                        for email in b.values():
                            for i in email:
                                if (i == event['username']):
                                    # m = RawMessage()
                                    # m.set_body(str({event['username']): 'TRUE'}))
                                    # q.write(m)
                                    connectdb.loginAttempts.find_one_and_replace(
                                        {"_id": ObjectId(event["aid"])},
                                        {"status": "success"}
                                    )
                                    return "Successful login"

    # m = RawMessage()
    connectdb.loginAttempts.find_one_and_replace(
        {"_id": ObjectId(event["aid"])},
        {"status": "error"}
    )
    # m.set_body({event['username']: 'FALSE'})
    # q.write(m)
    return "Invalid Username/Password"
