from flaskr import app
from flask import render_template
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
    videos = Videos.query.all()

    return render_template("routes/cursos.html", videos=videos)

@app.route("/cursos/clase/<int:video_id>", methods=["GET"])
def videos(video_id):
    """ Funcion para mostrar los videos de lass clases """
    videos = Videos.query.all()
    video = Videos.query.filter_by(id=video_id).first()

    return render_template("routes/videos.html", video=video, videos=videos)

@app.route("/perfil/<string:username>", methods=["GET"])
@login_required
def perfil(username):
    """ Funcion para mostrar el perfil de usuario """
    current_user = Users.query.filter_by(username=username).first()

    return render_template("routes/perfil.html", current_user=current_user)
