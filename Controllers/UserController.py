from flask import Flask, jsonify, request, Response, Blueprint
import pymongo
from bson import json_util, objectid
from bson.objectid import ObjectId
import datetime
import json
import os

user = Blueprint('user', __name__)

client = pymongo.MongoClient( os.environ['MONGODB_URI'] )
mongo = client.myFirstDatabase

@user.route('/login', methods=['POST'])
def user_login():

    content = request.json

    # Validate if data is complete.
    try:
        email = content['email']
        pwd = content['password']
    except KeyError as e:
        # Build Response.
        response = jsonify({'message': 'You are missing the %s field.' % e})
        response.status_code = 400
        return response
    except:
        return "Something is wrong with the json that you try to submit."
    
    # String validation in name, image, description and date. 
    if (not (type(email).__name__ == 'str' and  type(pwd).__name__ == 'str')):
        # Build Response.
        response = jsonify({'message': 'name, image, description and date field must be a string.'})
        response.status_code = 415
        return response

    find_user = mongo.users.find_one({'email':email})
    if (find_user is None):
        # Build Response.
        response = jsonify({'message': email + ' doesn''t exists.'})
        response.status_code = 404
        return response


    # Update likes in post.
    find_user_response = json_util.dumps(find_user)
    find_user_result = json.loads(find_user_response)

    if find_user_result['password'] == pwd:
        # Build Response.
        response = jsonify({'message': 'Success.'})
        response.status_code = 200
        return response

    # Build Response.
    response = jsonify({'message': 'email or password are incorrect.'})
    response.status_code = 404
    return response

@user.route('/signin', methods=['POST'])
def user_signin():

    content = request.json

    # Validate if data is complete.
    try:
        username = content['username']
        email = content['email']
        pwd = content['password']
        address = content['address']
        profileImage = content['profileImage']
        pets = content['pets']
    except KeyError as e:
        # Build Response.
        response = jsonify({'message': 'You are missing the %s field.' % e})
        response.status_code = 400
        return response
    except:
        return "Something is wrong with the json that you try to submit."
    
    # String validation in name, image, description and date. 
    if (not (type(username).__name__ == 'str' and  type(email).__name__ == 'str' and  type(pwd).__name__ == 'str' and  type(address).__name__ == 'str' and  type(profileImage).__name__ == 'str' )):
        # Build Response.
        response = jsonify({'message': 'name, image, description and date field must be a string.'})
        response.status_code = 415
        return response

    if (not(type(pets).__name__ == 'list')):
        # Build Response.
        response = jsonify({'message': 'pets field must be a list.'})
        response.status_code = 415
        return response

    find_user = mongo.users.find_one({'email':email})
    if (find_user is None):
        # Build Response.
        post_id = mongo.users.insert_one({ 'username': username,
                                         'email': email,
                                         'password': pwd,
                                         'address': address,
                                         'profileImage': profileImage,
                                         'pets': pets,
                                         'date': datetime.datetime.now() }).inserted_id
        # Build Response.
        response = jsonify({'message': str(post_id) + ' user created successfully.'})
        response.status_code = 201

        return response   
    
    response = jsonify({'message': email + ' exists. Try with a another one'})
    response.status_code = 404
    return response

@user.route('/<id>', methods=['DELETE'])
def DeleteUser(id):
    
    # Check if the id exists.
    post = mongo.users.find_one({'_id': ObjectId(id), })
    if (post is None):
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    mongo.users.delete_one({'_id': ObjectId(id)})
    
    # Build Response.
    response = jsonify({'message': id + ' deleted Successfully'})
    response.status_code = 200
    
    return response

@user.route('/username/<id>', methods=['PATCH'])
def PatchUsername(id):
    # Check if the id exists.
    find_post = mongo.users.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    content = request.json

    # Validate if data is complete.
    try:
        username = content['username']
        
        # Bool validation in like.
        if (not type(username).__name__ == 'str' ):
            # Build Response.
            response = jsonify({'message': 'username must be a string.'})
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
    update_post = mongo.users.update_one( {'_id': ObjectId(id), }, { "$set": { 'username': username, }})
    
    # Build Response.
    response = jsonify({'message': id + ' username updated Successfully'})
    response.status_code = 202
    
    return response

@user.route('/password/<id>', methods=['PATCH'])
def PatchPassword(id):
    # Check if the id exists.
    find_post = mongo.users.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    content = request.json

    # Validate if data is complete.
    try:
        password = content['password']
        
        # Bool validation in like.
        if (not type(password).__name__ == 'str' ):
            # Build Response.
            response = jsonify({'message': 'password must be a string.'})
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
    update_post = mongo.users.update_one( {'_id': ObjectId(id), }, { "$set": { 'password': password, }})
    
    # Build Response.
    response = jsonify({'message': id + ' password updated Successfully'})
    response.status_code = 202
    
    return response

@user.route('/address/<id>', methods=['PATCH'])
def PatchAdress(id):
    # Check if the id exists.
    find_post = mongo.users.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    content = request.json

    # Validate if data is complete.
    try:
        address = content['address']
        
        # Bool validation in like.
        if (not type(address).__name__ == 'str' ):
            # Build Response.
            response = jsonify({'message': 'address must be a string.'})
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
    update_post = mongo.users.update_one( {'_id': ObjectId(id), }, { "$set": { 'address': address, }})
    
    # Build Response.
    response = jsonify({'message': id + ' address updated Successfully'})
    response.status_code = 202
    
    return response

@user.route('/profileImage/<id>', methods=['PATCH'])
def PatchProfileImage(id):
    # Check if the id exists.
    find_post = mongo.users.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    content = request.json

    # Validate if data is complete.
    try:
        profileImage = content['profileImage']
        
        # Bool validation in like.
        if (not type(profileImage).__name__ == 'str' ):
            # Build Response.
            response = jsonify({'message': 'profile image must be a string.'})
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
    update_post = mongo.users.update_one( {'_id': ObjectId(id), }, { "$set": { 'profileImage': profileImage, }})
    
    # Build Response.
    response = jsonify({'message': id + ' profile image updated Successfully'})
    response.status_code = 202
    
    return response

@user.route('/pets/<id>', methods=['PATCH'])
def PatchPets(id):
    # Check if the id exists.
    find_post = mongo.users.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response

    content = request.json

    # Validate if data is complete.
    try:
        pets = content['pets']
        
        # Bool validation in like.
        if (not type(pets).__name__ == 'list' ):
            # Build Response.
            response = jsonify({'message': 'pets must be an array of string.'})
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
    update_post = mongo.users.update_one( {'_id': ObjectId(id), }, { "$set": { 'pets': pets, }})
    
    # Build Response.
    response = jsonify({'message': id + ' pets updated Successfully'})
    response.status_code = 202
    
    return response