from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util, objectid
from bson.objectid import ObjectId

import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/DispMov'
mongo = PyMongo(app)

@app.route('/persons', methods=['GET'])
def persons():
    users = mongo.db.persons.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/persons/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.persons.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/persons/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)
