import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources 
api = Api()

def create_app():

    app = Flask(__name__)
    load_dotenv()
    
    
    api.add_resource(resources.CalificationResource, '/calificacion/<id>')
    api.add_resource(resources.CalificationsResource, '/califications')
    api.add_resource(resources.PoemResource, '/poema/<id>')
    api.add_resource(resources.PoemsResource, '/poemas')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')
    api.init_app(app)
    return app