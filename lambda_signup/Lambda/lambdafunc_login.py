import sys
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo

conn = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
db = conn.userdb



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
                return "Successful login"

    return "Invalid Username/Password"
