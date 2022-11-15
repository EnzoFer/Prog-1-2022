from flask import Flask
from flask import FlaskForm
from wtforms import PassWordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators


class LoginForm(FlaskForm):
    email