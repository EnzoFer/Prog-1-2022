from flask_restful import Resource
from flask import request

USUARIOS = {
    1 : {'firstname' : 'A', 'lastname' : 'AAA'},
    2 : {'firstname' : 'B', 'lastname' : 'BBB'},
    
}

class User(Resource):
    def get(self, id):
        if int(id) in USUARIOS:
            return USUARIOS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in USUARIOS:
            return USUARIOS[int(id)]
        return '', 404
    
    def put(self, id):
        if int(id) in USUARIOS:
            user = USUARIOS[int(id)]
            data = request.get_json()
            user.update(data)
            return user, 201
        return '', 404

class Users(Resource):
    def get(self):
        return USUARIOS

    def post(self):
        user = request.get_json()
        id = int(max(USUARIOS.key())) + 1
        USUARIOS[id] = user
        return USUARIOS[id], 201