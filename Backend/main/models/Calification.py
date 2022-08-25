from .. import db



class Calification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puntaje = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    poem_id = db.Column(db.String(100), db.ForeignKey('poem.id'), nullable=False)

    user = db.relationship("User", back_populates= "califications", uselist=False, single_parent=True)
    poem = db.relationship("Poem", back_populates= "califications",uselist=False, single_parent=True)

    def __repr__(self):
        return f'<Puntaje: {self.puntaje}, Comentario: {self.comentario}, User: {self.user_id}, Poema: {self.poem_id}>'
    
    def to_json_complete(self):
        user = [users.to_json() for users in self.user]
        poem = poem.to_json()
        calification_json = {
            'id': self.id,
            'firstname': str(self.firstname),
            'password': str(self.password),
            'rol': str(self.rol),
            'email': str(self.email),
            'poem' : poem,
            'user': user

        }
        return calification_json

    def to_json(self):
        calification_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario),
            'user_id': self.user_id,
            'poem_id': self.poem_id       
        }
        return calification_json
            

            

    
    @staticmethod
    def from_json(calification_json):
        id = calification_json.get('id')
        puntaje = calification_json.get('puntaje')
        comentario = calification_json.get('comentario')
        user_id = calification_json.get('user_id')
        poem_id = calification_json.get('poem_id')

        return Calification(id=id,
                    puntaje=puntaje,
                    comentario=comentario,
                    user_id=user_id,
                    poem_id=poem_id
                    )