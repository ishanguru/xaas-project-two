from pymongo import MongoClient
import boto.ses
from bson.objectid import ObjectId
import json


connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb

verificationconn = boto.ses.connect_to_region(
         'us-east-1',
         aws_access_key_id='',
         aws_secret_access_key='')

def lambda_handler(event, context):
    print "EVENT"
    print event
    if (event["verifymail"]["id"] != "DONTSENDANEMAIL"):
        verification = event["verifymail"]["username"]

        verificationconn.send_email(
             'nachi.2605@gmail.com',
             'Verify your email PLEASE.',
             'https://7mdamwt4jg.execute-api.us-east-1.amazonaws.com/prod2/' + event["verifymail"]["id"] ,
             [verification])
    else:
        return ("No sign up sucker")


    return ("Verification mail has been sent")