from flask import Flask, render_template, request, jsonify,app, session
import stripe
import os
import boto3
from sqs_services import SQSServices
from pymongo import MongoClient
from datetime import timedelta
import json
import requests
from bson.objectid import ObjectId
from bson import json_util
import yaml

stripe_keys = {
  'secret_key': 'sk_test_Hrqp4whe1ZsCTyLzol7jth8v',
  'publishable_key': 'pk_test_mLVxfSZ0XoplPi6EppPDVic9'
}

stripe.api_key = stripe_keys['secret_key']

application = Flask(__name__)
application.debug = True
application.config['SECRET_KEY'] = 'super-secret'

connectdb = MongoClient('mongodb://user1:user1password@ds149030.mlab.com:49030/charge_db')["charge_db"]

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

    # send order to user info microservice to store stuff into db
    status = request.post('https://ec2-52-15-159-218.us-east-2.compute.amazonaws.com:5000/order', json=transaction)
    print "COOL STUFF BRO"
    # return "COOL STUFF BRO"
    return status

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    port = int(os.getenv('PORT', 8080)) 
    host = os.getenv('IP', '0.0.0.0')
    application.run(port=port, host=host)


