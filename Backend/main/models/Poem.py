from .. import db
import statistics, datetime as dt

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=dt.datetime.now())


    user = db.relationship("User", back_populates = "poems", uselist= False, single_parent= True)
    califications = db.relationship("Calification", back_populates = "poem", cascade = "all, delete-orphan")

    def __repr__(self):
        return '<Poem: %r %r >' % (self.id, self.titulo, self.user_id, self.cuerpo, self.fecha)

    def promedio_calificaciones(self):
        lista_calificaciones = []
        
        if len (self.califications) == 0:
            promedio = 0
        else:    
            for calification in self.califications:
                puntaje = calification.puntaje
                lista_calificaciones.append(puntaje)
            promedio = statistics.mean(lista_calificaciones)
        return promedio

    def to_json(self):
        poem_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'autor': self.user.to_json(),
            'cuerpo': str(self.cuerpo),
            'fecha': str(self.fecha.strftime("%d-%m-%Y")),
            'califications': [calification.to_json() for calification in self.califications],
            'promedio_calificaciones': self.promedio_calificaciones()
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id, 
            'titulo': self.titulo,
            'cuerpo': self.cuerpo        
        }
        return poem_json

    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        titulo = poem_json.get('titulo')
        user_id = poem_json.get('user_id')
        cuerpo = poem_json.get('cuerpo')
        return Poem(id=id,
                    titulo=titulo,
                    user_id=user_id,
                    cuerpo=cuerpo
                    )