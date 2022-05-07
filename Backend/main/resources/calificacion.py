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
        #califications = db.session.query(CalificationModel).all()
        #return jsonify([calification.to_json_short() for calification in califications])
        pag = 1
        p_pag = 10
        califications = db.session.query(CalificationModel)


        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:

                if key == "pag":
                    pag = int(value)

                if key == "p_pag":
                    p_pag = int(value)

                if key == "puntaje":
                    puntaje = puntaje.filter(CalificationModel.puntaje == value)
                
                if key == "comentario":
                    comentario = comentario.filter(CalificationModel.comentario.like("%" + value + "%"))
                
                if key == "poemID":
                    poemID = poemID.filter(CalificationModel.poemID == value)
                
                if key == "poemID":
                    poemID = poemID.filter(CalificationModel.poemID == value)
                
                if key == "sort_by":
                    
                    if value == "puntaje":
                        puntaje = puntaje.order_by(CalificationModel.puntaje)
                    
                    if value == "puntaje[desc]":
                        puntaje = puntaje.order_by(CalificationModel.puntaje.desc())
                    
                    if value == "userID":
                        userID = userID.order_by(CalificationModel.userID)
                    
                    if value == "userId[des]":
                        userID = userID.order_by(CalificationModel.userID.desc())
                    
                    if value == "poemID":
                        poemID = poemID.order_by(CalificationModel.poemID)
                    
                    if value == "poemID[des]":
                        poemID = poemID.order_by(CalificationModel.poemID.desc())
                        
                
        califications = califications.paginate(pag, p_pag, False, 30)


        
    def post(self):
        calification = CalificationModel.from_json(request.get_json())
        db.session.add(calification)
        db.session.commit()
        return calification.to_json(), 201
