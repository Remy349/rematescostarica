import os

class Config(object):
    """ Clase para las configuraciones de la app """
    # Clase secreta para las sesiones de usuarios
    SECRET_KEY=os.getenv("SECRET_KEY")
    # Llamado de la uri a la base de datos y configuraciones de sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Configuracion para las sesiones
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
