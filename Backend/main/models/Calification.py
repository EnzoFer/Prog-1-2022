from .. import db



class Calification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puntaje = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.String(100), nullable=False)
    userID = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    poemID = db.Column(db.String(100), db.ForeignKey('poem.id'), nullable=False)

    author = db.relationship("User", back_populates= "calification", uselist=False, single_parent=True)
    poem = db.relationship("Poem", back_populates= "calification",uselist=False, single_parent=True)

    def __repr__(self):
        return f'<Puntaje: {self.puntaje}, Comentario: {self.comentario}, User: {self.userID}, Poema: {self.poemID}>'
    def to_json(self):
            calification_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario),
            'userID': str(self.userID),
            'poemID': str(self.poemID),                
            }
            return calification_json

    def to_json_complete(self):
        user = [users.to_json() for users in self.user]
        poem = poem.to_json()
        calification_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario),
            'userID': str(self.userID),
            'poemID': str(self.poemID),
            'poem' : poem,
            'user': user

        }
        return calification_json

    
    
    @staticmethod
    def from_json(calification_json):
        id = calification_json.get('id')
        puntaje = calification_json.get('puntaje')
        comentario = calification_json.get('comentario')
        userID = calification_json.get('userID')
        poemID = calification_json.get('poemID')

        return Calification(id=id,
                    puntaje=puntaje,
                    comentario=comentario,
                    userID=userID,
                    poemID=poemID
                    )