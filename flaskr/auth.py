from flaskr import app
from flask import render_template, redirect, url_for, request

@app.route("/registrate", methods=["GET", "POST"])
def registrate():
    """ Funcion para manejar y realizar el proceso de registro de un nuevo usuario """
    if request.method == "GET":
        return render_template("auth/registrate.html")
    elif request.method == "POST":
        return redirect(url_for("index"))
