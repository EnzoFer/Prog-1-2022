from flask import Blueprint, render_template

poema = Blueprint('poema', __name__, url_prefix="/poema")

@poema.route('/')
def index():
    return render_template('poem.html')

@poema.route('/poema/<id>')
def poem(id):
    return render_template('poem.html')