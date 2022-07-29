import os
from datetime import timedelta

class Config(object):
    """ Clase para las configuraciones de la app """
    # Clase secreta para las sesiones de usuarios
    SECRET_KEY=os.getenv("SECRET_KEY")
    # Llamado de la uri a la base de datos y configuraciones de sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Configuracion para las sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_TYPE = "filesystem"
    # Configuracion para subir archivos temporalmente al servidor
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
