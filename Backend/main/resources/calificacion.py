from flask import request
from flask_restful import Resource

CALIFICACIONES = {
    1 : {'calification' : 1},
    2 : {'calification' : 2},
    3 : {'calification' : 3},
    4 : {'calification' : 4},
    5 : {'calification' : 5},
    
}

class Calification(Resource):
    def get(self, id):
        if int(id) in CALIFICACIONES:
            return CALIFICACIONES[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in CALIFICACIONES:
            return CALIFICACIONES[int(id)]
        return '', 404

class Califications(Resource):
    def get(self):
        return CALIFICACIONES

    def post(self):
        calification = request.get_json()
        id = int(max(CALIFICACIONES.key())) + 1
        CALIFICACIONES[id] = calification
        return CALIFICACIONES[id], 201