from datetime import datetime
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
    gravatar = db.Column(db.String(120), nullable=False, unique=True)
    payment_completed = db.Column(db.String(40), nullable=False)
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
                Gravatar: {self.gravatar},
                Payment_completed: {self.payment_completed}
        """

class Videos(db.Model):
    """ Tabla para guardar la url de los videos del curso """
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True, unique=False)
    public_id = db.Column(db.String(140), nullable=False)
    url_video = db.Column(db.String(180), nullable=False, unique=True)
    path_video = db.Column(db.String(140), nullable=False)
    filename_video = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"""
            Video:
                Id: {self.id},
                Title: {self.title},
                Description: {self.description},
                PublicId: {self.public_id},
                UrlVideo: {self.url_video},
                PathVideo: {self.path_video},
                FilenameVideo: {self.filename_video}
        """

class Posts(db.Model):
    """ Tabla para que el usuario admin pueda guardar sus publicaciones """
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(200), nullable=False)
    user_image = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"""
            Posts:
                Id: {self.id},
                Title: {self.title},
                Description: {self.description},
                UserImage: {self.user_image},
                Timestamp: {self.timestamp}
        """

class Admin(db.Model):
    """ Tabla para super usuario """
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(160), nullable=False)
    email_adress = db.Column(db.String(160), nullable=False, unique=True)
    gravatar = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f"""
            Admin:
                Id: {self.id},
                Firstname: {self.firstname},
                Lastname: {self.lastname},
                Username: {self.username},
                Email_adress: {self.email_adress},
                Gravatar: {self.gravatar}
        """
