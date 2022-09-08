from main.routes import routes
from flask import Flask
from dotenv import load_dotenv



def create_app():
    app=Flask(__name__)
    load_dotenv()
    app.register_blueprint(routes.app)
    return app
