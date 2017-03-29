import sys
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo

conn = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')

db = conn.userdb
#mongo = PyMongo(conn)

def login():

    users = db.users
    login_user = users.find_one({'name' : request.form['inputEmail']})

    if login_user:
        if request.form['inputPassword'] == login_user['password'] :
            session['inputEmail'] = request.form['inputEmail']
            email = request.form['inputEmail']

            # payload = {'iss': email}
            payload = {'iss': email, 'exp': 30000000000, 'admin': True}

            token = jwt.encode(
            payload,
            application.config.get('SECRET_KEY'),
            algorithm='HS256')

            tokentoken = token

            userhistory = db.userhistory
            currentHistory = list(userhistory.find({"name" : email}))

# def register():
#     print('registering user')
#     if request.method == 'POST':
#         try:
#             users = mongo.db.users
#             existing_user = users.find_one({'name' : request.form['inputEmail']})
#         except:
#             print "failed to find user"
#
#         if existing_user is None:
#             print('creating user')
#             hashpass = request.form['inputPassword']
#             users.insert({'name' : request.form['inputEmail'], 'password' : hashpass})
#             session['inputEmail'] = request.form['inputEmail']
#             email = request.form['inputEmail']
#
#             # payload = {'iss': email}
#             payload = {'iss': email, 'exp': 30000000000, 'admin': True}
#
#             token = jwt.encode(
#             payload,
#             application.config.get('SECRET_KEY'),
#             algorithm='HS256')
#
#             tokentoken = token
#
#             userhistory = mongo.db.userhistory
#             currentHistory = list(userhistory.find({"name" : email}))
#
#             return render_template('index3.html', email=email, token=token, history=currentHistory)
#
#         return 'That inputEmail already exists!'
# #





def lambda_handler(event, context):
    def register():
        print('registering user')
        if request.method == 'POST':
            try:
                users = db.users
                existing_user = users.find_one({'name' : request.form['inputEmail']})
            except:
                print ("failed to find user")

            if existing_user is None:
                print('creating user')
                hashpass = request.form['inputPassword']
                users.insert({'name' : request.form['inputEmail'], 'password' : hashpass})
                session['inputEmail'] = request.form['inputEmail']
                email = request.form['inputEmail']

                payload = {'iss': email, 'exp': 30000000000, 'admin': True}

                token = jwt.encode(
                payload,
                application.config.get('SECRET_KEY'),
                algorithm='HS256')

                tokentoken = token

                userhistory = db.userhistory
                currentHistory = list(userhistory.find({"name" : email}))


            return 'That inputEmail already exists!'
    #




    return "Connection Successful with the database"

#    return "Added %d items from RDS MySQL table" %(item_count)
