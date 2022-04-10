from flaskr import app
from flask import render_template

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
