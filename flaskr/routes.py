from flaskr import app, db
from flask import render_template, session, redirect, url_for, request
from helpers import login_required
from werkzeug.security import generate_password_hash

from flaskr.models import Users, Videos, Posts, ContentPage

@app.route("/", methods=["GET"])
def index():
    """ Funcion para mostrar la pagina principal """
    posts = Posts.query.order_by(Posts.id.desc()).all()
    content_page_home_one = ContentPage.query.filter_by(from_page="home", \
            from_section="1").all()
    content_page_home_two = ContentPage.query.filter_by(from_page="home", \
            from_section="2").all()

    return render_template("index.html", posts=posts, content_page_home_one=content_page_home_one, \
            content_page_home_two=content_page_home_two)

@app.route("/quienes_somos", methods=["GET"])
def quienes_somos():
    """ Funcion para mostrar la pagina de ¿quienes somos? """
    content_page_about_one = ContentPage.query.filter_by(from_page="quienes_somos", \
            from_section="1").all()

    return render_template("routes/quienes_somos.html", content_page_about_one=content_page_about_one)

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
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email_adress = request.form["email_adress"]
        phonenumber = request.form["phonenumber"]
        postal_code = request.form["postal_code"]
        adress = request.form["adress"]
        password_value = request.form["password"]

        current_user = Users.query.filter_by(username=username).first()
        videos = Videos.query.all()

        if password_value == "" or password_value == " ":
            current_user.firstname = firstname
            current_user.lastname = lastname
            current_user.email_adress = email_adress
            current_user.phonenumber = phonenumber
            current_user.postal_code = postal_code
            current_user.adress = adress
        else:
            current_user.firstname = firstname
            current_user.lastname = lastname
            current_user.email_adress = email_adress
            current_user.phonenumber = phonenumber
            current_user.postal_code = postal_code
            current_user.adress = adress
            current_user.password_hash = generate_password_hash(password_value)

        db.session.add(current_user)
        db.session.commit()

        return render_template("routes/perfil.html", current_user=current_user, videos=videos)
