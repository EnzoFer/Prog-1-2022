from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    poem = db.relationship("Poem", back_populates= "author", cascade="all, delete-orphan")
    calification = db.relationship("Calification", back_populates= "author", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Usuario: %r %r >' % (self.id, self.firstname, self.password, self.rol, self.email)
   
    def to_json(self):
        poem = [poem.to_json() for poem in self.poems]
        calification = [calification.to_json() for calification in self.califications]
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'password': self.password,
            'rol' : self.rol,
            'email': self.email,
            'poema' : poem,
            'calificacion': calification

        }
        return user_json


    def to_json_short(self):
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'rol' : self.rol
        }
        return user_json
    
    @staticmethod    
    def from_json(user_json):
        id = user_json.get('id')
        firstname = user_json.get('firstname')
        password = user_json.get('password')
        rol = user_json.get('rol')
        email = user_json.get('email')
        return User (id = id,
            firstname = firstname,
            password = password,
            rol = rol,
            email =email)
