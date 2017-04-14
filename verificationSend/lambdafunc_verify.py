from pymongo import MongoClient
import boto.ses
from bson.objectid import ObjectId
import json


connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb

verificationconn = boto.ses.connect_to_region(
         'us-east-1',
         aws_access_key_id='AKIAJMUE6DERO7DRYJGA',
         aws_secret_access_key='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')

def lambda_handler(event, context):
    verification = event["username"]
    current_status = connectdb.signupAttempts.find_one({"_id": ObjectId(event["aid"])})
    print (current_status)
    if (current_status["status"] == "undefined"):
        verificationconn.send_email(
             'nachi.2605@gmail.com',
             'Verify your email PLEASE.',
             'https://7mdamwt4jg.execute-api.us-east-1.amazonaws.com/prod2/' + event["_id"] ,
             [verification])
    else:
        return ("No sign up sucker")


    return ("Verification mail has been sent")
