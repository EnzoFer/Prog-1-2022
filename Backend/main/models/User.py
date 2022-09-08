from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    poems = db.relationship("Poem", back_populates= "user", cascade="all, delete-orphan")
    califications = db.relationship("Calification", back_populates= "user", cascade="all, delete-orphan")

    

    @property
    def plain_password(self):
        raise AttributeError('Error al leer la contraseña')

    @plain_password.setter
    def plain_password(self, secret):
        self.password = generate_password_hash(secret)


    def validate_pass(self,secret):
        return check_password_hash(str(self.password) , str (secret))




    def __repr__(self):
        return '<Usuario: %r %r >' % (self.id, self.firstname, self.password, self.rol, self.email)
   
    def to_json_complete(self):
        poems = [poem.to_json() for poem in self.poems]
        califications = [calification.to_json() for calification in self.califications]
        user_json = {
            'id': self.id,
            'firstname': self.firstname,
            'password': self.password,
            'rol' : self.rol,
            'email': self.email,
            'califications': califications,
            'poems': poems,
            'n_poems': len(self.poems),
            'n_puntaje': len(self.puntaje)
            
        }
        return user_json

    def to_json(self):
        user_json = {
            'id': self.id,
            'firstname': str(self.firstname),
            'email': str(self.email),
            'rol': str(self.rol),
            'n_poems': len(self.poems),
            'n_califications': len(self.califications),
            'poems': [poem.to_json() for poem in self.poems]
            
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
            plain_password = password,
            rol = rol,
            email =email)
    