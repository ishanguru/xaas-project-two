from flask import Flask, render_template, request, jsonify,app, session
import stripe
import os
import boto3
from sqs_services import SQSServices
from pymongo import MongoClient
from datetime import timedelta
import json
import requests

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
    # print(notification)

    if headers == 'SubscriptionConfirmation' and 'SubscribeURL' in notification:
        url = requests.get(notification['SubscribeURL'])
        # print(url) 
    elif headers == 'Notification':
        chargeStatus = charge(notification)
    else: 
        print("Headers not specified")

    if chargeStatus:
        return "Payment Processed\n"
        
    return "SNS Notification Recieved\n"  

@application.route('/getpayment', methods=['GET'])
def getPayment():
    caid = request.form["aid"]
    paymentObject = connectdb.caids.find_one({"_id": ObjectId(str(caid))})
    return paymentObject

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

    connectdb.caids.find_one_and_replace({"_id": ObjectId(str(caid))},{"status": "success"})
    transaction = jsonify(result)

    # send order to user info microservice to store stuff into db
    status = request.post('https://ec2-52-15-159-218.us-east-2.compute.amazonaws.com:5000/order', json=transaction)

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


