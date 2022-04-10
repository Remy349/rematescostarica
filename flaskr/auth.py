from flaskr import app
from flask import render_template, redirect, url_for, request

@app.route("/registrate", methods=["GET", "POST"])
def registrate():
    """ Funcion para manejar y realizar el proceso de registro de un nuevo usuario """
    if request.method == "GET":
        return render_template("auth/registrate.html")
    elif request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        phonenumber = request.form["phonenumber"]
        email_adress = request.form["email_adress"]
        adress = request.form["adress"]
        postal_code = request.form["postal_code"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        return redirect(url_for("cursos"))

@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    """ Funcion para realizar el inicio de sesion de cada usuario """
    if request.method == "GET":
        return render_template("auth/iniciar_sesion.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        return redirect(url_for("cursos"))
