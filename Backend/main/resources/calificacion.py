from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificationModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt



class Calification(Resource):
    def get(self, id):
        calification = db.session.query(CalificationModel).get_or_404(id)
        return calification.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        userID = get_jwt_identity()             
        calification = db.session.query(CalificationModel).get_or_404(id)
        if "rol" in claims:
            if claims['rol'] == "admin" or userID == calification.userID:
                db.session.delete(calification)
                db.session.commit()
                return '', 204
            else:
                return "error"
    
    @jwt_required()
    def put(self, id):
        userID = get_jwt_identity()
        calification = db.session.query(CalificationModel).get_or_404(id)
        if userID == calification.userID:
            data = request.get_json().items()
            for key, value in data:
                setattr(calification,key,value)
            db.session.add(calification)
            db.session.commit()
            return calification.to_json(), 201
        else:
            return "error"


class Califications(Resource):
    def get(self):
        califications = db.session.query(CalificationModel).all()
        return jsonify([calification.to_json() for calification in califications])
        
    @jwt_required()
    def post(self):
        calification = CalificationModel.from_json(request.get_json())
        claims = get_jwt()
        if "rol" in claims:
            if claims ["rol"] == "poet":
                db.session.add(calification)
                db.session.commit()
                return calification.to_json(), 201
            
            else:
                return "xxxx"