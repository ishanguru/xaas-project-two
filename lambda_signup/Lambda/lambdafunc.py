import sys
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
import email
import jwt

## Connection with the MongoDB
connectdb = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
db = connectdb.userdb




def verificationemail():
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(me, you, msg.as_string())
    s.quit()

## Set up existing AWS SQS
conf = {

}


import boto.sqs
from boto.sqs.message import RawMessage

conn = boto.sqs.connect_to_region(
        conf.get('sqs-region'),
        aws_access_key_id   = conf.get('sqs-access-key'),
        aws_secret_access_key   = conf.get('sqs-secret-key')
)

q = conn.get_queue('queue_signup')


def lambda_handler(event, context):

    users = db.users
    existing_user = users.find_one({'name' : event['username']})
    if existing_user:
        m = RawMessage()
        m.set_body({'event['username']' : 'FALSE'})
        q.write(m)
        return 'That inputEmail already exists!'
    else:
        print('creating user for', event['username'] )
        hashpass = event['password']
        users.insert({'name' : event['username'], 'password' : hashpass})
        m = RawMessage()
        m.set_body({'event['username']' : 'TRUE'})
        q.write(m)

        return " Successful Registration"
            #userhistory = db.userhistory
            #currentHistory = list(userhistory.find({"name" : email}))
