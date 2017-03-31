from pymongo import MongoClient
import boto.sns
import boto.ses
import boto.sqs
from boto.sqs.message import RawMessage
## Connection with the MongoDB
connectdb = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
db = connectdb.userdb


botoconn = boto.sns.connect_to_region( 'us-east-1' )





verificationconn = boto.ses.connect_to_region(
        'us-east-1',
        aws_access_key_id='AKIAJN3ACGV3J6SG3Q5A',
        aws_secret_access_key='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')

## Set up existing AWS SQS
conf = { "sqs-access-key": "AKIAJN3ACGV3J6SG3Q5A",
"sqs-secret-key": "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",
"sqs-queue-name": "queue_signup",
"sqs-region": "us-east-1",
"sqs-path": "sqssend"

}

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
        m.set_body({ str(event['username']) : 'FALSE'})
        q.write(m)
        return 'That inputEmail already exists!'
    else:
        print('creating user for', event['username'] )
        hashpass = event['password']
        users.insert({'name' : event['username'], 'password' : hashpass})
        m = RawMessage()
        m.set_body({ str(event['username']) : 'TRUE'})
        q.write(m)
        verificationconn.verify_email_address(event['username'])
        return " Successful Registration"
