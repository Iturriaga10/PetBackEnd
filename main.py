from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util, objectid
from bson.objectid import ObjectId

import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Pets'
mongo = PyMongo(app)

@app.route('/feed', methods=['GET'])
def allFeed():
    users = mongo.db.feed.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/feed/<id>', methods=['GET'])
def feedById(id):
    user = mongo.db.feed.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/feed', methods=['POST'])
def PostFeed():

    content = request.json

    # Validate if data is complete.
    try:
        name = content['name']
        image = content['image']
        description = content['description']
        like = content['like']
    except KeyError as e:
        return "You are missing the %s field." % e
    except:
        return "Something is wrong with the json that you try to submit."
    
    # String validation in name, image, description and date. 
    if (not (type(name).__name__ == 'str' and  type(image).__name__ == 'str' and type(description).__name__ == 'str' )):
        # Build Response.
        response = jsonify({'message': 'name, image, description and date field must be a string.'})
        response.status_code = 415
        return response

    # Bool validation in like.
    if (not type(like).__name__ == 'bool' ):
        response = jsonify({'message': 'like must be a bool.'})
        response.status_code = 415
        return response
    
    post_id = mongo.db.feed.insert_one({ 'name': name,
                                         'image': image,
                                         'description': description,
                                         'like': like,
                                         'date': datetime.datetime.now() }).inserted_id
    # Build Response.
    response = jsonify({'message': str(post_id) + ' posetd successfully.'})
    response.status_code = 201

    return response

@app.route('/feed/<id>', methods=['DELETE'])
def DeleteFeed(id):
    
    # Check if the id exists.
    post = mongo.db.feed.find_one({'_id': ObjectId(id), })
    if (post is None):
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    mongo.db.feed.delete_one({'_id': ObjectId(id)})
    
    # Build Response.
    response = jsonify({'message': id + ' deleted Successfully'})
    response.status_code = 200
    
    return response

@app.route('/feed/image/<id>', methods=['PATCH'])
def PatchImageFeed(id):
    
    # Check if the id exists.
    find_post = mongo.db.feed.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    content = request.json

    # Validate if data is complete.
    try:
        image = content['image']
        
        # Bool validation in like.
        if (not type(image).__name__ == 'str' ):
            # Build Response.
            response = jsonify({'message': 'image must be a string.'})
            response.status_code = 415
            return response

    except KeyError as e:
        # Build Response.
        response = jsonify({'message': 'You are missing the %s field.' % e})
        response.status_code = 400
        return response
    except:
        return "Something is wrong with the json that you try to submit."
    
    # Update post.
    update_post = mongo.db.feed.update_one( {'_id': ObjectId(id), }, { "$set": { 'image': image, }})
    
    # Build Response.
    response = jsonify({'message': id + ' image updated Successfully'})
    response.status_code = 202
    
    return response

@app.route('/feed/description/<id>', methods=['PATCH'])
def PatchDescriptionFeed(id):
    
    # Check if the id exists.
    find_post = mongo.db.feed.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    content = request.json

    # Validate if data is complete.
    try:
        description = content['description']
        
        # Bool validation in like.
        if (not type(description).__name__ == 'str' ):
            # Build Response.
            response = jsonify({'message': 'description must be a string.'})
            response.status_code = 415
            return response

    except KeyError as e:
        # Build Response.
        response = jsonify({'message': 'You are missing the %s field.' % e})
        response.status_code = 400
        return response
    except:
        return "Something is wrong with the json that you try to submit."
    
    # Update post.
    update_post = mongo.db.feed.update_one( {'_id': ObjectId(id), }, { "$set": { 'description': description, }})
    
    # Build Response.
    response = jsonify({'message': id + ' description updated Successfully'})
    response.status_code = 202
    
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
