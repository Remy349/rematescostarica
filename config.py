import os

class Config(object):
    """ Clase para las configuraciones de la app """
    SECRET_KEY=os.getenv("SECRET_KEY")
