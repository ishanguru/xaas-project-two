from pymongo import MongoClient
import boto.ses
from bson.objectid import ObjectId
import json

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb

verificationconn = boto.ses.connect_to_region(
         'us-east-1',
         aws_access_key_id='',
         aws_secret_access_key='')

def lambda_handler(event, context):
    verification = event["username"]
    # gmail_user = 'tradewizardmailing@gmail.com'
    # gmail_pwd = 'ILOVEASE2'
    # FROM = 'tradewizardmailing@gmail.com'
    # TO = verification
    # SUBJECT = 'T.'
    # TEXT = 'How are we doing today'
    # message = "Sending" + TEXT
    #
    # print (verification)
    # try:
    #     server = smtplib.SMTP("smtp.googlemail.com", 465)
    #     server.ehlo()
    #     server.starttls()
    #     server.startssl()
    #     server.login(gmail_user, gmail_pwd)
    #     server.sendmail(FROM, TO, message)
    #     server.close()
    #     print ('successfully sent the mail')
    # except:
    #     print ("failed to send mail")


    # requests.post(
    #         "https://api.mailgun.net/v3/sandbox451a8c8f4bd046389400e6ed13801b32.mailgun.org/messages",
    #         auth=("api", "key-229420542ec1e27b172be8315555b8fd"),
    #         data={"from": "Mailgun Sandbox <nachi.2605@gmail.com>",
    #               "to": verification,
    #               "subject": "Verification Email",
    #               "text": "Congratulations Nachiket, you just sent an email with Mailgun!  You are truly awesome! NOT."})

    verificationconn.send_email(
             'nachi.2605@gmail.com',
             'Verify your email PLEASE.',
             'Enter the Lambda function here',
             [verification])
    return ("Verification mail has been sent")
