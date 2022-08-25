from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import CalificationModel

import datetime
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt



class Poem(Resource):
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()


    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_id = get_jwt_identity() 
        poem = db.session.query(PoemModel).get_or_404(id)
        if "rol" in claims:
            if claims["rol"] == "admin" or user_id == int(poem.user_id):
                db.session.delete(poem)
                db.session.commit()
                return '', 204
            else:
                return "xxxx"        
    

class Poems(Resource):
    @jwt_required(optional=True)
    def get(self):
        poems = db.session.query(PoemModel)
        pag = 1
        p_pag = 10
        claims = get_jwt()
        identify_user = get_jwt_identity()
        if identify_user:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                    if key == "pag":
                        pag = int(value)
                    
                    if key == "p_pag":
                        p_pag = int(value)
            poems = db.session.query(PoemModel).filters(PoemModel.user_id != identify_user)
            poems = poems.outerjoin(PoemModel.califications).group_by(PoemModel.id).order_by(func.count(PoemModel.califications))



        else:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                
                    if key == "pag":
                        pag = int(value)
                
                    if key == "p_pag":
                        p_pag = int(value)
                
                    if key == "titulo":
                        poems = poems.filter(PoemModel.titulo.like('%'+value+'%'))
                
                    if key == "user_id":
                        poems = poems.filter(PoemModel.user_id ==value)
                    
                    if key == "firstname":
                        poems = poems.user_name(PoemModel.user.has(UserModel.firstname.like('%'+value+'%')))
                    
                    if key == "created[gt]":
                        poems = poems.filter(PoemModel.fecha >= datetime.strptime(value, '%d-%m-%Y'))
                
                    if key == "created[lt]":
                        poems = poems.filter(PoemModel.fecha <= datetime.strptime(value, '%d-%m-%Y'))


                    if key == "sort_by":
                    
                        if value == "author":
                            poems = poems.order_by(PoemModel.user)
                    
                        if value == "author[desc]":
                            poems = poems.order_by(PoemModel.user.desc())
                    
                        if value == "fecha":
                            poems == poems.order_by(PoemModel.fecha)
                    
                        if value == "fecha[desc]":
                            poems = poems.order_by(PoemModel.fecha.desc())
                    
                        if value == "calification":
                            poems = poems.outerjoin(PoemModel.califications).group_by(PoemModel.id).order_by(func.mean(CalificationModel.puntaje))
                    
                        if value == "calification[desc]":
                            poems = poems.outerjoin(PoemModel.califications).group_by(PoemModel.id).order_by(func.mean(CalificationModel.puntaje).desc())
            
            
        poems = poems.paginate(pag, p_pag, False, 30)

        if "rol" in claims:
            if claims ["rol"] == "admin":
                return jsonify({
                        "poems" : [poem.to_json() for poem in poems.items],
                        "total" : poems.total,
                        "pages" : poems.pages,
                        "page" : pag
                        })

        else:
            return jsonify({
                        "poems" : [poem.to_json_short() for poem in poems.items],
                        "total" : poems.total,
                        "pages" : poems.pages,
                        "page" : pag
                        })


    @jwt_required()
    def post(self):
        user_id = get_jwt_identity
        poem = PoemModel.from_json(request.get_json())
        user = db.session.query(UserModel).get_or_404(user_id)
        claims = get_jwt()
        if "rol" in claims:
            if claims ["rol"] == "poet":
                if len(user.poems) == 0 or len (user.calications) >= 2:
                    poem.user_id = user_id
                    db.session.add(poem)
                    db.session.commit()
                    return poem.to_json(), 201
                else:
                    return "aaa"
            else:
                return "eeee"


        