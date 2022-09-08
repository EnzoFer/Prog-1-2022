from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel, UserModel
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from main.auth.decorators import admin_required




class User(Resource):
    @jwt_required(optional=True)
    def get(self, id):
        user_id = get_jwt_identity()
        user = UserModel.from_json(request.get_json())
        user = db.session.query(UserModel).get_or_404(user_id)
        claims = get_jwt()
        if 'rol' in claims:
            if claims["rol"] == "admin":
                user.user_id = user_id
                db.session.add(user)
                db.session.commit()
                return user.to_json(), 201
        else:
            return user.to_json_short(), 201
      

    @jwt_required() 
    def delete(self, id):   
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    @jwt_required()
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json() , 201



class Users(Resource):
    @admin_required
    def get(self):
        user = db.session.query(UserModel)
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

                if key == "email":
                    users = users.filter(UserModel.email.like('%'+value+'%'))
                
                if key == "sort_by":
            
                    if key == 'firstname':
                        users = users.order_by(UserModel.firstname)
            
                    if value == "n_user[desc]":
                        users = users.outerjoin(UserModel.users).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
            
                    if value == "n_user":
                        users = users.outerjoin(UserModel.users).group_by(UserModel.id).order_by(func.count(UserModel.id))
            
                    if value == "n_califications":
                        users = users.outerjoin(UserModel.califications).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
        
        users = users.paginate(pag, p_pag, True, 30)
        
        return jsonify({
            'users' : [user.to_json() for user in users.items],
            'total' : users.total,
            'pages' : users.pages,
            'pag' : pag
        })
    @admin_required
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
