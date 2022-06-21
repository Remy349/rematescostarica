from flaskr import app
from flask import render_template, session, redirect, url_for, request
from helpers import login_required

from flaskr.models import Users, Videos

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
    username = session.get("username")

    if username is None:
        current_user = { "payment_completed": "Sin Adquirir" }
        videos = Videos.query.all()

        return render_template("routes/cursos.html", videos=videos, current_user=current_user)
    else:
        videos = Videos.query.all()
        current_user = Users.query.filter_by(username=username).first()

        return render_template("routes/cursos.html", videos=videos, current_user=current_user)

@app.route("/cursos/clase/<int:video_id>", methods=["GET"])
@login_required
def videos(video_id):
    """ Funcion para mostrar los videos de lass clases """
    videos = Videos.query.all()
    video = Videos.query.filter_by(id=video_id).first()

    return render_template("routes/videos.html", video=video, videos=videos)

@app.route("/cursos/comprar", methods=["GET"])
@login_required
def comprar_curso():
    """ Funcion para mostrar una unica vista dde la compra del curso """
    username = session.get("username")

    current_user = Users.query.filter_by(username=username).first()

    if current_user.payment_completed == "Sin Adquirir":
        return render_template("routes/comprar_curso.html")
    else:
        return redirect(url_for("perfil", username=username))

@app.route("/perfil/<string:username>", methods=["GET"])
@login_required
def perfil(username):
    """ Funcion para mostrar el perfil de usuario """
    current_user = Users.query.filter_by(username=username).first()
    videos = Videos.query.all()

    return render_template("routes/perfil.html", current_user=current_user, videos=videos)

@app.route("/perfil/<string:username>/editar", methods=["GET", "POST"])
@login_required
def editar_perfil(username):
    """ Ruta para poder editar el perfil de los usuarios """
    if request.method == "GET":
        current_user = Users.query.filter_by(username=username).first()

        return render_template("routes/editar_perfil.html", current_user=current_user)
    elif request.method == "POST":
        pass
