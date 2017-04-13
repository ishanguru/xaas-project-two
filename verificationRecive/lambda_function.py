from pymongo import MongoClient
import boto.ses
from bson.objectid import ObjectId

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb
users = db.users

verificationconn = boto.ses.connect_to_region(
    'us-east-1',
    aws_access_key_id='',
    aws_secret_access_key='')

def lambda_handler(event, context):
    return event
    userId = event["params"]["path"]["userId"]
    if userId[0] == '"' and userId[-1] == '"':
        userId = userId[1:-1]
    users.update_one(
        {"_id": ObjectId(userId)},
        {"status": "verified"}
    )
    return "registered!"
