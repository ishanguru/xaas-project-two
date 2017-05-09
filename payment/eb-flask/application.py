from flask import Flask, render_template, request, jsonify,app, session
import stripe
import os
import boto3
# from sqs_services import SQSServices
from pymongo import MongoClient
from datetime import timedelta
import json
import requests
from bson.objectid import ObjectId
from bson import json_util
import yaml
from boto3 import Session
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))

awsAccessKey=config.get('AWS Keys', 'awsAccessKeyId')
awsSecretKey=config.get('AWS Keys', 'awsSecretAccessKeyId')
awsRegion=config.get('AWS Keys', 'awsRegion')
stripeSecretKey=config.get('STRIPE Keys', 'stripeSecretKey')
stripePublishableKey=config.get('STRIPE Keys', 'stripePublishableKey')

stripe_keys = {
  'secret_key': stripeSecretKey,
  'publishable_key': stripePublishableKey
}

aws_session = Session(
    aws_access_key_id=awsAccessKey,
    aws_secret_access_key=awsSecretKey,
    region_name=awsRegion,
)

stripe.api_key = stripe_keys['secret_key']

application = Flask(__name__)
application.debug = True
application.config['SECRET_KEY'] = 'super-secret'

connectdb = MongoClient('mongodb://user1:user1password@ds149030.mlab.com:49030/charge_db')["charge_db"]

# Set up SQS connection to queue
try:
    sqs_queue = aws_session.client('sqs')
except Exception as e:
    print("Queue already exists")


@application.route('/sns', methods = ['GET', 'POST', 'PUT'])
def snsFunction():
    try:
        notification = json.loads(request.data)
    except:
        print("Unable to load request")
        pass

    
    headers = request.headers.get('X-Amz-Sns-Message-Type')

    if headers == 'SubscriptionConfirmation' and 'SubscribeURL' in notification:
        url = requests.get(notification['SubscribeURL'])
    elif headers == 'Notification':
        temp = json.loads(str(notification['Message']))
        charge(temp)
    else: 
        print("Headers not specified")
        
    return "SNS Notification Recieved\n"  

@application.route('/getpayment', methods=['GET', 'POST'])
def getPayment():
    temp = yaml.load(request.data)
    caid = temp["aid"]
    paymentObject = connectdb.caids.find_one({"_id": ObjectId(str(caid))})
    toSend = json.dumps(paymentObject, default=json_util.default)
    return toSend

#stripe
@application.route('/payment', methods=['POST'])
def charge(notification):
    # Amount in cents
    print(notification)

    amount = notification["amount"]
    caid = notification["aid"]
    email = notification["email"]
    source=notification["id"]
    
    customer = stripe.Customer.create(
        email=email,
        source=source
    )

    try:
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )

        connectdb.caids.find_one_and_replace({"_id": ObjectId(str(caid))},{"status": "success"})
        pass
    except Exception as e:
        print "Error making payment"
    
    result = {}
    result['status'] = charge['status']
    result['amount'] = charge['amount']
    result['email'] = notification['email']

    transaction = jsonify(result)

    # Since we have the caid, I can get the object and add it to the queue right here, so this is the object that is retrieved upon poll

    paymentsQueueUrl = sqs_queue.get_queue_url(QueueName='ordersQueue')
    paymentObject = connectdb.caids.find_one({"_id": ObjectId(str(caid))})
    
    queueResponse = sqs_queue.send_message(
        QueueUrl=paymentsQueueUrl, 
        Message=json.loads(paymentObject),
        MessageAttributes={
            'caid': {
                'StringValue': str(caid),
                'DataType': 'string'
            }
        }
    )
    print paymentsqueue
    print json.loads(paymentObject)

    # send order to user info microservice to store stuff into db
    # add order to user info microservice queue
    status = request.post('https://ec2-52-15-159-218.us-east-2.compute.amazonaws.com:5000/order', json=transaction)
    print "COOL STUFF BRO"
    # return "COOL STUFF BRO"
    return status

# @application.route('/sqs', methods=['GET'])
# def getQueue():
#     paymentsQueue = sqs_queue.get_queue_url(QueueName='ordersQueue')
#     print paymentsQueue
#     return str(paymentsQueue)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    port = int(os.getenv('PORT', 8080)) 
    host = os.getenv('IP', '0.0.0.0')
    application.run(port=port, host=host)


