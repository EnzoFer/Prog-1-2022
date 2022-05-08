from .. import db
from datetime import datetime
from sqlalchemy import func
from statistics import mean


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime(timezone=True), default=func.now())


    author = db.relationship("User", back_populates = "poem", uselist= False, single_parent= True)
    calification = db.relationship("Calification", back_populates = "poem", cascade = "all, delete-orphan")

    def __repr__(self):
        return '<Poem: %r %r >' % (self.id, self.titulo, self.user_id, self.cuerpo, self.fecha)

    def promedio_calificaciones(self):
        lista_calificaciones = []
        promedio = 0
        if len (lista_calificaciones) >= 1:
            for calification in self.calification       :
                puntaje = calification.puntaje
                lista_calificaciones.append(puntaje)
                promedio = statistics.mean(lista_calificaciones)
            return promedio

    def to_json(self):
        calification = [calification.to_json() for calification in self.calification]
        poem_json = {
            'id': self.id,
            'titulo': self.titulo,
            'user_id': self.user_id,
            'cuerpo': self.cuerpo,
            'fecha': str(self.fecha.strftime("%d-%m-%Y")),
            'calification': self.calification,
            'promedio_calificaciones': self.promedio_calificaciones()
        }
        return poem_json

      
    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        titulo = poem_json.get('titulo')
        user_id = poem_json.get('user_id')
        cuerpo = poem_json.get('cuerpo')
        fecha = poem_json.get('fecha')
        return Poem(id=id,
                    titulo=titulo,
                    user_id=user_id,
                    cuerpo=cuerpo,
                    fecha=fecha
                    )