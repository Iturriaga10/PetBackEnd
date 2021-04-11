from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint
from bson import json_util, objectid
from bson.objectid import ObjectId
import datetime
import logging
import os
import json

# Define logger.
LOGGER = logging.getLogger(__name__)

# Import enviroment variables.
if os.path.exists('.env'):
    LOGGER.info("Using .env file")
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

# Initialize Flask.
app = Flask(__name__)
# app.register_blueprint(simple_page)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/Pets'

app.config['MONGO_URI'] = os.environ['MONGODB_URI']
                           

mongo = PyMongo(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

@app.route('/swagger', methods=['GET'])
def send_swagger():
    response = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Dogstagram"
        }
    )

    return render_template(response)

@app.route('/static/<path:path>', methods=['GET'])
def send_static():
    return  send_from_directory('static', path)
### end swagger specific ###

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
    except KeyError as e:
        # Build Response.
        response = jsonify({'message': 'You are missing the %s field.' % e})
        response.status_code = 400
    except:
        return "Something is wrong with the json that you try to submit."
    
    # String validation in name, image, description and date. 
    if (not (type(name).__name__ == 'str' and  type(image).__name__ == 'str' and type(description).__name__ == 'str' )):
        # Build Response.
        response = jsonify({'message': 'name, image, description and date field must be a string.'})
        response.status_code = 415
        return response
    
    post_id = mongo.db.feed.insert_one({ 'name': name,
                                         'image': image,
                                         'description': description,
                                         'like': False,
                                         'likeCounter': 0,
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

@app.route('/feed/like/increase/<id>', methods=['PUT'])
def IncreaseLikesFeed(id):
    
    # Check if the id exists.
    find_post = mongo.db.feed.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response
    
    # Update likes in post.
    update_post = mongo.db.feed.update_one( {'_id': ObjectId(id), }, { "$inc": { 'likeCounter': 1, }})
    
    # Build Response.
    response = jsonify({'message': id + ' likeCounter updated Successfully'})
    response.status_code = 202
    
    return response

@app.route('/feed/like/decrease/<id>', methods=['PUT'])
def DecreaseLikesFeed(id):

    # Check if the id exists.
    find_post = mongo.db.feed.find_one({'_id': ObjectId(id), })
    if (find_post is None):
        # Build Response.
        response = jsonify({'message': id + ' doesn''t exists.'})
        response.status_code = 404
        return response
    
    # Update likes in post.
    find_post_response = json_util.dumps(find_post)
    find_post_result = json.loads(find_post_response)
    

    if find_post_result['likeCounter'] == 0:
        response = jsonify({'message': 'likeCounter can''t be lower than 0.'})
        response.status_code = 404
        return response
    
    update_post = mongo.db.feed.update_one( {'_id': ObjectId(id), }, { "$inc": { 'likeCounter': -1, }})
    
    # Build Response.
    response = jsonify({'message': id + ' likeCounter updated Successfully'})
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
