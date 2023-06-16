from flask import Blueprint

bp = Blueprint("admin", __name__)

from flaskr.admin import dashboard
from flaskr.admin import usuarios
from flaskr.admin import pagos
from flaskr.admin import cursos
from flaskr.admin import editar_pagina
from flaskr.admin import configuraciones
