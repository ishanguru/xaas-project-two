from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
import boto.ses
import boto.sns
import json

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb

# verificationconn = boto.ses.connect_to_region(
#     'us-east-1',
#     aws_access_key_id='AKIAIYILDTN5HSKGIAOA',
#     aws_secret_access_key='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')
#
# verifiedemails = verificationconn.list_verified_email_addresses()


def lambda_handler(event, context):

    #if polling
    if "type" in event and event["type"] == "loginQuery":
        matchingAttempt = connectdb.loginAttempts.find_one({"_id": ObjectId(event["aid"])})

        dictToReturn = {}
        dictToReturn["status"] = str(matchingAttempt["status"])
        dictToReturn["aid"] = str(matchingAttempt["_id"])

        if dictToReturn["status"] == "success":
            # get username and password
            password = connectdb.users.find_one({"name": str(event["email"])})["password"]
            userJwt = jwt.encode({'email' : event["email"],'password' : password}, 'secret', algorithm='HS256')
            dictToReturn["jwt"] = userJwt
        return dictToReturn

    users = db.users

    if ("Records" in event):
        event = event["Records"][0]["Sns"]["Message"]

    event = json.loads(str(event))

    print "This is the event!"
    print event

    login_user = users.find_one({'name': event['username'], 'password': event['password']})
    if login_user and login_user["status"] and login_user["status"]=="verified":
        connectdb.loginAttempts.find_one_and_replace(
            {"_id": ObjectId(event["aid"])},
            {"status": "success"}
        )
        return "Successful login"
    else:
        connectdb.loginAttempts.find_one_and_replace(
            {"_id": ObjectId(event["aid"])},
            {"status": "error"}
        )
        return "Invalid Username/Password"
