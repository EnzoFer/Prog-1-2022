from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<Usuario: %r %r >' % (self.id, self.firstname, self.password, self.rol, self.email)
   
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'firstname': str(self.firstname),
            'password': str(self.password),
            'rol' : str(self.rol),
            'email': str(self.email),

        }
        return usuario_json


    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'firstname': str(self.firstname),
            'password': str(self.password),
            'rol' : str(self.rol),
            'email': str(self.email),

        }
        return usuario_json
    
    @staticmethod    
    def from_json(usuario_json):
        id = usuario_json.get('id')
        firstname = usuario_json.get('firstname')
        password = usuario_json.get('password')
        rol = usuario_json.get('rol')
        email = usuario_json.get('email')
        return Users (id = id,
            firstname = firstname,
            password = password,
            rol = rol,
            email =email)
