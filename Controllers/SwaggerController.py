from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import os

simple_page = get_swaggerui_blueprint(
        os.environ['SWAGGER_URL'],
        os.environ['API_URL'],
        config={
            'app_name': "PetStagram"
        }
    )