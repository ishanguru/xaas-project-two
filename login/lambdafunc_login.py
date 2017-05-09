from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
import boto.ses
import boto.sns
import json

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb


def lambda_handler(event, context):
    # return "hello"
    # if polling
    print "this is the event"
    # return event
    if not event:
        return "no event :("

    if event and "loginid" in event:
        matchingAttempt = connectdb.loginAttempts.find_one({"_id": ObjectId(event["loginid"])})

        dictToReturn = {}
        dictToReturn["status"] = str(matchingAttempt["status"])
        dictToReturn["aid"] = str(matchingAttempt["_id"])

        if dictToReturn["status"] == "success":
            # get username and password
            password = connectdb.users.find_one({"name": str(matchingAttempt["username"])})["password"]
            userJwt = jwt.encode({'email': str(matchingAttempt["username"]), 'password': password}, 'secret',
                                 algorithm='HS256')
            dictToReturn["jwt"] = userJwt
        return dictToReturn

    users = db.users

    if ("Records" in event):
        event = event["Records"][0]["Sns"]["Message"]

    event = json.loads(str(event))

    print "This is the event!"
    print event

    login_user = users.find_one({'name': event['username'], 'password': event['password']})
    if login_user and login_user["status"] and login_user["status"] == "verified":
        connectdb.loginAttempts.find_one_and_replace(
            {"_id": ObjectId(event["aid"])},
            {"status": "success",
             "username": event['username'],
             "password": event["password"]}
        )
        return "Successful login"
    else:
        connectdb.loginAttempts.find_one_and_replace(
            {"_id": ObjectId(event["aid"])},
            {"status": "error"}
        )
        return "Invalid Username/Password"
