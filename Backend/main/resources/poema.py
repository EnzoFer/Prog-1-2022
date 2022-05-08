from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import CalificationModel

import datetime
from sqlalchemy import func

class Poem(Resource):
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()

    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '', 204

    

class Poems(Resource):
    def get(self):
        poems = db.session.query(PoemModel)
        pag = 1
        p_pag = 10
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
            
                if key == "pag":
                    pag = int(value)
            
                if key == "p_pag":
                    p_pag = int(value)
            
                if key == "titulo":
                    poems = poems.filter(PoemModel.titulo.like('%'+value+'%'))
            
                if key == "author":
                    poems = poems.filter(PoemModel.author ==value)
                
                if key == "created[gt]":
                    poems = poems.filter(PoemModel.fecha >= datetime.strptime(value, '%d-%m-%Y'))
            
                if key == "created[lt]":
                    poems = poems.filter(PoemModel.fecha <= datetime.strptime(value, '%d-%m-%Y'))


                if key == "sort_by":
                
                    if value == "author":
                        poems = poems.order_by(PoemModel.author)
                
                    if value == "author[desc]":
                        poems = poems.order_by(PoemModel.author.desc())
                
                    if value == "fecha":
                        poems == poems.order_by(PoemModel.fecha)
                
                    if value == "fecha[desc]":
                        poems = poems.order_by(PoemModel.fecha.desc())
                
                    if value == "calification":
                        poems = poems.outerjoin(PoemModel.calification).group_by(PoemModel.id).order_by(func.avg(CalificationModel.puntaje))
                
                    if value == "calification[desc]":
                        poems = poems.outerjoin(PoemModel.calification).group_by(PoemModel.id).order_by(func.avg(CalificationModel.puntaje).desc())
        poems = poems.paginate(pag, p_pag, False, 30)

               
        return jsonify({
                "poems" : [poem.to_json() for poem in poems.items],
                "total" : poems.total,
                "pages" : poems.pages,
                "page" : pag
                })

        
    def post(self):
        poem = PoemModel.from_json(request.get_json())
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201