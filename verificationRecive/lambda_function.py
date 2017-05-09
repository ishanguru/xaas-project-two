from pymongo import MongoClient
import boto.ses
from bson.objectid import ObjectId
import requests
import json

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb
users = db.users

verificationconn = boto.ses.connect_to_region(
    'us-east-1',
    aws_access_key_id='',
    aws_secret_access_key='')

def lambda_handler(event, context):
    userId = event["params"]["path"]["userId"]
    if userId[0] == '"' and userId[-1] == '"':
        userId = userId[1:-1]
    connectdb.users.update_one(
        {"_id": ObjectId(userId)},
        {'$set': {'status': 'verified'}}
    )

    new_user = users.find_one({'_id' : ObjectId(userId)})
    name = new_user['name'];
    # POST to Slack channel
    requests.post("https://hooks.slack.com/services/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", 
        data=json.dumps({"text":"A New User has been registered: \n" + name}))

    return "registered!"
