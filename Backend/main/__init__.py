import os
from flask import Flask
from dotenv import load_dotenv
#Importar librería flask_restful
from flask_restful import Api
#Importar SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#Inicializar API de Flask Restful
api = Api()
#Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    #Si no existe el archivo de base de datos crearlo (solo válido si se utiliza SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Url de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)


    import main.resources as resources


    
    api.add_resource(resources.CalificationResource, '/calificacion/<id>')
    api.add_resource(resources.CalificationsResource, '/califications')
    api.add_resource(resources.PoemResource, '/poema/<id>')
    api.add_resource(resources.PoemsResource, '/poemas')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')
    api.init_app(app)
    return app