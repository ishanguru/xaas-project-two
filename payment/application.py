from flask import Flask, render_template, request, jsonify,app, session
import stripe
import os
# from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

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
        
#stripe
@application.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = request.form["amount"]
    print request.form

    customer = stripe.Customer.create(
        email=request.form['email'],
        source=request.form['id']
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

    return jsonify(result)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    port = int(os.getenv('PORT', 8080)) 
    host = os.getenv('IP', '0.0.0.0')
    application.run(port=port, host=host)

