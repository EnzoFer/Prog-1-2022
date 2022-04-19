from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificationModel



class Calification(Resource):
    def get(self, id):
        calification = db.session.query(CalificationModel).get_or_404(id)
        return calification.to_json()


    def delete(self, id):
        calification = db.session.query(CalificationModel).get_or_404(id)
        db.session.delete(calification)
        db.session.commit()
        return '', 204


class Califications(Resource):
    def get(self):
        califications = db.session.query(CalificationModel).all()
        return jsonify([calification.to_json_short() for calification in califications])

        
    def post(self):
        calification = CalificationModel.from_json(request.get_json())
        db.session.add(calification)
        db.session.commit()
        return calification.to_json(), 201
