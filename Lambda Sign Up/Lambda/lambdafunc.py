import sys
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
import email
import jwt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


conn = MongoClient('mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb')
db = conn.userdb


EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAJZRYVG2CUXLHPR6A'
EMAIL_HOST_PASSWORD = 'AjkRZ0Cav+/iNKubL+yfCpudvr2NA/YkRZ4myZ4eU6qB'
EMAIL_PORT = 587

msg = MIMEMultipart('alternative')
msg['Subject'] = "test foo"
msg['From'] = "nachi.2605@gmail.com"
msg['To'] = "nachi.2605@gmail.com"

me = u'nachi.2605@gmail.com'
you = ('nachi.2605@gmail.com', )


#html = open('index.html').read()

#mime_text = MIMEText(html, 'html')
mime_text = MIMEText("How are you doing today?")
msg.attach(mime_text)

s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
s.starttls()
s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
s.sendmail(me , you, msg.as_string())
s.quit()

def lambda_handler(event, context):

    print('registering user')
    try:
        users = db.users
        existing_user = users.find_one({'name' : event['username']})
    except:
        print ("failed to find user")

    if existing_user:

        return 'That inputEmail already exists!'

    else:

        print('creating user for', event['username'] )
        hashpass = event['password']
        users.insert({'name' : event['username'], 'password' : hashpass})
        return " Successful Registration"

    #

    #application.config.get('SECRET_KEY'),




#    return "Added %d items from RDS MySQL table" %(item_count)
