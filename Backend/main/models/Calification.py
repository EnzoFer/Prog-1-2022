from .. import db

class Calification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puntaje = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.String(100), nullable=False)
    userID = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    poemaID = db.Column(db.String(100), db.ForeignKey('poem.id'), nullable=False)

    def __repr__(self):
        return '<User: %r %r >' % (self.id, self.puntaje, self.comentario, self.userID, self.poemaID)

    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario),
            'userID': str(self.userID),
            'poemaID': str(self.poemaID),

        }
        return calificacion_json

    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario),
            'userID': str(self.userID),
            'poemaID': str(self.poemaID),
        }
        return calificacion_json
    
    @staticmethod

    def from_json(user_json):
        id = user_json.get('id')
        puntaje = user_json.get('puntaje')
        comentario = user_json.get('comentario')
        userID = user_json.get('userID')
        poemaID = user_json.get('poemaID')

        return Calification(id=id,
                    puntaje=puntaje,
                    comentario=comentario,
                    userID=userID,
                    poemaID=poemaID
                    )