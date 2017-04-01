from pymongo import MongoClient
import boto.sqs
from boto.sqs.message import RawMessage

connectdb = MongoClient('mongodb://user1:password@ds149040.mlab.com:49040/user_db')
db = connectdb.userdb

import boto.sns

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

import boto.ses

verificationconn = boto.ses.connect_to_region(
    'us-east-1',
    aws_access_key_id='AKIAJN3ACGV3J6SG3Q5A',
    aws_secret_access_key='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')

verifiedemails = verificationconn.list_verified_email_addresses()


def lambda_handler(event, context):

    #if polling
    if "type" in event and event["type"] == "loginQuery":
        return connectdb.loginAttempts.findOne({"_id": event["aid"]})

    users = db.users
    login_user = users.find_one({'name': event['username']})


    if login_user:
        if event['username'] == login_user['name']:
            if event['password'] == login_user['password']:
                for a in verifiedemails.values():
                    for b in a.values():
                        for email in b.values():
                            for i in email:
                                if (i == event['username']):
                                    m = RawMessage()
                                    m.set_body(str({event['username']): 'TRUE'})
                                    q.write(m)
                                    connectdb.loginAttempts.findOneAndReplace({
                                        {"_id": event["aid"]},
                                        {"status": "success"}
                                    })
                                    return "Successful login"

    m = RawMessage()
    connectdb.loginAttempts.findOneAndReplace({
        {"_id": event["aid"]},
        {"status": "error"}
    })
    m.set_body({event['username']: 'FALSE'})
    q.write(m)
    return "Invalid Username/Password"

