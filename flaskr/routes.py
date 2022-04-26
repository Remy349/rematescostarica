from flaskr import app
from flask import render_template
from helpers import login_required

from flaskr.models import Users

@app.route("/", methods=["GET"])
def index():
    """ Funcion para mostrar la pagina principal """
    return render_template("index.html")

@app.route("/quienes_somos", methods=["GET"])
def quienes_somos():
    """ Funcion para mostrar la pagina de ¿quienes somos? """
    return render_template("routes/quienes_somos.html")

@app.route("/cursos", methods=["GET"])
def cursos():
    """ Funcion para presentar la pagina de los cursos """
    return render_template("routes/cursos.html")

@app.route("/perfil/<string:username>", methods=["GET"])
@login_required
def perfil(username):
    """ Funcion para mostrar el perfil de usuario """
    current_user = Users.query.filter_by(username=username).first()

    return render_template("routes/perfil.html", current_user=current_user)
