from flaskr import app
from flask import render_template

@app.route("/", methods=["GET"])
def index():
    """ Funcion para mostrar la pagina principal """
    return render_template("index.html")
