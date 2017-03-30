import sys
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
import email
import jwt

## Connection with the MongoDB
connectdb = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
db = connectdb.userdb

## Configuration for the Amazon SES service
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAJZRYVG2CUXLHPR6A'
EMAIL_HOST_PASSWORD = 'AjkRZ0Cav+/iNKubL+yfCpudvr2NA/YkRZ4myZ4eU6qB'
EMAIL_PORT = 587


def verificationemail():
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(me, you, msg.as_string())
    s.quit()

## Set up existing AWS SQS
conf = {
  "sqs-access-key": "AKIAJN3ACGV3J6SG3Q5A",
  "sqs-secret-key": "amepI5y7KFJ0PpjiC5TNiai7OFjcpnRH+39k6jqL",
  "sqs-queue-name": "sample_queue1",
  "sqs-region": "us-east-1",
  "sqs-path": "sqssend"
}

import boto.sqs
from boto.sqs.message import RawMessage

conn = boto.sqs.connect_to_region(
        conf.get('sqs-region'),
        aws_access_key_id   = conf.get('sqs-access-key'),
        aws_secret_access_key   = conf.get('sqs-secret-key')
)


q = conn.create_queue(conf.get('sqs-queue-name'))

def lambda_handler(event, context):

    users = db.users
    existing_user = users.find_one({'name' : event['username']})


    if existing_user:
        m = RawMessage()
        m.set_body('FALSE')
        retval = q.write(m)
        return 'That inputEmail already exists!'
    else:
        print('creating user for', event['username'] )
        hashpass = event['password']
        users.insert({'name' : event['username'], 'password' : hashpass})
        m = RawMessage()
        m.set_body('TRUE')
        retval = q.write(m)

        return " Successful Registration"
            #userhistory = db.userhistory
            #currentHistory = list(userhistory.find({"name" : email}))
