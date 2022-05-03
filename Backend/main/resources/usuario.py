from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from sqlalchemy import func



class User(Resource):
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json() , 201



class Users(Resource):
    def get(self):
        users = db.session.query(UserModel)
        pag = 1
        p_pag = 10
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
            
                if key == "pag":
                    pag = int(value)
            
                if key == "p_pag":
                    p_pag = int(value)
            
                if key == "firstname":
                    users = users.filter(UserModel.firstname.like('%'+value+'%'))
                
                if key == "sort_by":
            
                    if key == 'firtname':
                        users = users.order_by(UserModel.firstname.like('%'+value+'%'))
            
                    if value == "npoems[desc]":
                        users = users.order_by(func.count(UserModel.id).desc())
            
                    if value == "num_poems":
                        users = users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(UserModel.id))
            
                    if value == "num_califications":
                        users = users.outerjoin(UserModel.califications).group_by(UserModel.id).order_by(func.count(UserModel.id))
        users = users.paginate(pag, p_pag, False, 30)
        return jsonify({
            'user' : [user.to_json_short() for user in users.items],
            'total' : users.total,
            'pages' : users.pages,
            'page' : pag
        })
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
