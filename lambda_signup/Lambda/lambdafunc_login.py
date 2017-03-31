import sys
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo

connectdb = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
db = connectdb.userdb

conf = {

}

import boto.sqs
from boto.sqs.message import RawMessage

conn = boto.sqs.connect_to_region(
        conf.get('sqs-region'),
        aws_access_key_id   = conf.get('sqs-access-key'),
        aws_secret_access_key   = conf.get('sqs-secret-key')
)

q = conn.get_queue('queue_login')



verificationconn = boto.ses.connect_to_region(
        'us-east-1',
        aws_access_key_id='AKIAJN3ACGV3J6SG3Q5A',
        aws_secret_access_key='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')

verifiedemails = verificationconn.list_verified_email_addresses()

def lambda_handler(event, context):

    users = db.users
    login_user = users.find_one({'name' : event['username']})

    print (event['username'])
    print (event['password'])
    print (login_user['name'])
    print (login_user['password'])

    if login_user:
        if event['username'] == login_user['name'] :
            if event['password'] == login_user['password']:
                email = verifiedemails.find_one({'VerifiedEmailAddresses': event['username']})
                if email:
                    m = RawMessage()
                    m.set_body({event['username'] : 'TRUE'})
                    q.write(m)
                    email = verifiedemails.find_one({'VerifiedEmailAddresses': event['username']})
                    return "Successful login"

    m = RawMessage()
    m.set_body({event['username'] : 'FALSE'})
    q.write(m)
    return "Invalid Username/Password"
