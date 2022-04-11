from flaskr import db
from werkzeug.security import check_password_hash, generate_password_hash

class Users(db.Model):
    """ Tabla para guardar los datos del usuario """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    phonenumber = db.Column(db.String(25), nullable=False)
    email_adress = db.Column(db.String(160), nullable=False, unique=True)
    adress = db.Column(db.String(160), nullable=True)
    postal_code = db.Column(db.String(60), nullable=True)
    password_hash = db.Column(db.String(160), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"""
            User:
                Id: {self.id},
                Firstname: {self.firstname},
                Lastname: {self.lastname},
                Username: {self.username},
                Phonenumber: {self.phonenumber},
                Email_adress: {self.email_adress},
        """
