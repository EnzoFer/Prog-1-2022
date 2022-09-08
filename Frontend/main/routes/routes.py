from re import template
from flask import Falsk, Blueprint, render_template

app = Blueprint('app', __name__, url_prefix="/")



@app.route('/')
def main():
    return render_template('main.html')

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

@app.route('/poem')
def poem():
    return render_template('poem.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/all_poems')
def all_poems():
    return render_template('all_poems.html')


