from .. import db
from datetime import datetime
from sqlalchemy import func


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)

    author = db.relationship("User", back_populates = "poem", uselist= False, single_parent= True)
    calification = db.relationship("Calification", back_populates = "poem", cascade = "all, delete-orphan")

    def __repr__(self):
        return '<Poem: %r %r >' % (self.id, self.titulo, self.user_id, self.cuerpo, self.fecha)

    def to_json(self):
        poem_json = {
            'id': self.id,
            'titulo': self.titulo,
            'user_id': self.user_id,
            'cuerpo': self.cuerpo,
            'fecha': self.fecha
        }
        return poem_json

      
    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        titulo = poem_json.get('titulo')
        user_id = poem_json.get('user_id')
        cuerpo = poem_json.get('cuerpo')
        fecha = poem_json.get('fehca')
        return Poem(id=id,
                    titulo=titulo,
                    user_id=user_id,
                    cuerpo=cuerpo,
                    fecha=fecha
                    )