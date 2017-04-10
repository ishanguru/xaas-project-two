from flask import Flask, render_template, request, jsonify,app, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
db = connectdb
users = db.users

application = Flask(__name__)

@app.route('/user/<userid>')
def show_user_profile(userid):
    users.update_one(
        {"_id": ObjectId(userid)},
        {"status": "verified"}
    )

    return 'Registered!'


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    application.run(port=port, host=host)