from flask import Flask
from dotenv import load_dotenv
import os


app = Flask (__name__)

if __name__ == '__main__':
    app.run(debug=True, port= 8000)
