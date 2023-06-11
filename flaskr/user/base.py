from flask import Blueprint

bp = Blueprint("user", __name__)

from flaskr.user import dashboard
from flaskr.user import configuraciones
