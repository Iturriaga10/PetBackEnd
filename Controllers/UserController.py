from flask import Blueprint, Response, Request
import pymongo
from bson import json_util, objectid
import os

user = Blueprint('user', __name__)

client = pymongo.MongoClient( os.environ['MONGODB_URI'] )
mongo = client.myFirstDatabase

@user.route('/login', methods=['GET'])
def user_login():
    users = mongo.feed.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')
    