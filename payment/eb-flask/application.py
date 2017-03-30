from flask import Flask, render_template, request, jsonify,app, session
import stripe
import os
import boto3
from sqs_services import SQSServices
# from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import json
import requests

stripe_keys = {
  'secret_key': 'sk_test_Hrqp4whe1ZsCTyLzol7jth8v',
  'publishable_key': 'pk_test_mLVxfSZ0XoplPi6EppPDVic9'
}

stripe.api_key = stripe_keys['secret_key']

# EB looks for an 'application' callable by default.
application = Flask(__name__)
# application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://p1backend:project1databasepasswordformad@p1madinstance.cukjopk8vvdd.us-west-2.rds.amazonaws.com:5432/madp1db'
# db = SQLAlchemy(application)

application.debug = True
application.config['SECRET_KEY'] = 'super-secret'

#sqs
try:
    sqs_queue = SQSServices()
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
    # print(notification)

    if headers == 'SubscriptionConfirmation' and 'SubscribeURL' in notification:
        url = requests.get(notification['SubscribeURL'])
        # print(url) 
    elif headers == 'Notification':
        charge(notification)
    else: 
        print("Headers not specified")

    return "SNS Notification Recieved\n"  

#stripe
@application.route('/payment', methods=['POST'])
def charge(notification):
    # Amount in cents
    amount = notification["amount"]
    print notification

    customer = stripe.Customer.create(
        email=notification['email'],
        source=notification['id']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    result = {}
    result['status'] = charge['status']
    result['amount'] = charge['amount']
    result['email'] = notification['email']

    transaction = jsonify(result)

    queue_name = sqs_queue.getQueueName('paymentsQueue')
    response = queue_name.send_message(MessageBody=transaction, MessageAttributes={
            'email': {
                'StringValue': notification['email'],
                'DataType': 'String'
            }    
        })

    # send order to user info microservice to store stuff into db
    # status = request.post('http://ENDPOINT' json=transaction)

    return "COOL STUFF BRO"
    # return status

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    port = int(os.getenv('PORT', 8080)) 
    host = os.getenv('IP', '0.0.0.0')
    application.run(port=port, host=host)

