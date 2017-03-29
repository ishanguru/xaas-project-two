from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import jwt
from datetime import datetime

from flask_cors import CORS, cross_origin

application = Flask(__name__,template_folder='templates')

CORS(application)

application.config['MONGO_DBNAME'] = 'userdb'
application.config['MONGO_URI'] = 'mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb'
application.secret_key = 'newsecret'

mongo = PyMongo(application)

tokentoken = None

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

@application.route('/order', methods=['POST', 'GET'])
def payment():

    currentUser = request.form['stripeEmail']

    cartTotal = float(request.form['cartTotal'])

    userhistory = mongo.db.userhistory
    now = str(datetime.date(datetime.now()))

    userhistory.insert_one({"name": currentUser, "TransactionAmount": cartTotal, "TransactionTime": now})

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
