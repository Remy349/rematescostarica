from flask import Blueprint

bp = Blueprint("admin", __name__)

from flaskr.admin import dashboard
from flaskr.admin import cursos