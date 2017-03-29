import sys
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
import email
import jwt

conn = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
db = conn.userdb


EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAJZRYVG2CUXLHPR6A'
EMAIL_HOST_PASSWORD = 'AjkRZ0Cav+/iNKubL+yfCpudvr2NA/YkRZ4myZ4eU6qB'
EMAIL_PORT = 587


def verificationemail():
    # verificationlink =

    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(me, you, msg.as_string())
    s.quit()

def lambda_handler(event, context):

    #def register():
    print('registering user')
    try:
        users = db.users
        existing_user = users.find_one({'name' : event['username']})
    except:
        print ("failed to find user")

    #if existing_user is None:
    print('creating user for', event['username'] )
    hashpass = event['password']
    users.insert({'name' : event['username'], 'password' : hashpass})

    #session['name'] = event['username']
    #email = request.form['inputEmail']

    payload = {'iss': email, 'exp': 30000000000, 'admin': True}

    # token = jwt.encode(
    # payload, 'SECRET_KEY',
    # algorithm='HS256')
    #
    # tokentoken = token
    return " Successful Registration"
            #userhistory = db.userhistory
            #currentHistory = list(userhistory.find({"name" : email}))


    return 'That inputEmail already exists!'
    #

    #application.config.get('SECRET_KEY'),




#    return "Added %d items from RDS MySQL table" %(item_count)
