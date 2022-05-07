from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel




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
                if key == "firstname":
                    users = users.filter(UserModel.firstname.like('%'+value+'%'))

                if key == "email":
                    users = users.filter(UserModel.email.like('%'+value+'%'))
                
                if key == "sort_by":
            
                    if key == 'firstname':
                        users = users.order_by(UserModel.firstname.like('%'+value+'%'))
            
                    if value == "firstname[desc]":
                        users = users.order_by(UserModel.firstname.desc())
            
                    if value == "email":
                        users = users.order_by(UserModel.email)
            
                    if value == "email[desc]":
                        users = users.order_by(UserModel.email.desc())
        
        users = users.paginate(pag, p_pag, False, 30)
        
        return jsonify({
            'poems' : [users.to_json_short() for users in users.items],
            'total' : users.total,
            'pages' : users.pages,
            'page' : pag
        })
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
