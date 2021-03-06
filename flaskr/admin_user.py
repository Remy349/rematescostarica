import os
from flaskr import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from helpers import login_required
from openpyxl import Workbook
from cloudinary.uploader import upload_large, destroy
from werkzeug.utils import secure_filename

from flaskr.models import Admin, Users, Videos

ALLOWED_EXTENSIONS = {"mp4", "mp3"}

def allowed_file(filename):
    """ Funcion para validar la extension de los videos a subir """
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/iniciar_sesion_admin", methods=["GET", "POST"])
def iniciar_sesion_admin():
    """ Funcion para el inicio de sesion del usuario admin """
    if request.method == "GET":
        if "username" in session:
            return redirect(url_for('usuario_admin'))
        else:
            return render_template("admin/iniciar_sesion_admin.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        errors = None

        admin_user = Admin.query.filter_by(username=username).first()

        if admin_user is None:
            errors = "Nombre de usuario incorrecto!"
        elif not check_password_hash(admin_user.password, password):
            errors = "Contraseña incorrecta!"

        if errors is None:
            session["user_id"] = admin_user.id
            session["username"] = admin_user.username
            session["gravatar"] = admin_user.gravatar
            session.permanent = True
            return redirect(url_for("usuario_admin"))

        if errors:
            flash(errors)
            return redirect(url_for("iniciar_sesion_admin"))

@app.route("/perfil/usuario_admin", methods=["GET"])
@login_required
def usuario_admin():
    """ Funcion para mostrar el perfil del usuario admin del sitio """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("perfil", username=username))
    else:
        admin_user = Admin.query.filter_by(username=username).first()
        videos = Videos.query.all()
        users = Users.query.all()

        total_users = 0
        payment_completed_users = 0
        payment_uncompleted_users = 0

        for user in users:
            total_users = total_users + 1

            if user.payment_completed == "Sin Adquirir":
                payment_uncompleted_users = payment_uncompleted_users + 1

            if user.payment_completed == "Adquirido":
                payment_completed_users = payment_completed_users + 1

        total_data_info = {
            "total_users": total_users,
            "payment_completed_users": payment_completed_users,
            "payment_uncompleted_users": payment_uncompleted_users,
        }

        return render_template("admin/usuario_admin.html", admin_user=admin_user, videos=videos, users=users, \
                               total_data_info=total_data_info)

@app.route("/perfil/usuario_admin/agregar_video", methods=["GET", "POST"])
@login_required
def agregar_video():
    """ Ruta para agregar videos nuevos para el curso """
    if request.method == "GET":
        username = session.get("username")

        if username != os.getenv("ADMIN_USERNAME"):
            return redirect(url_for("perfil", username=username))
        else:
            return render_template("admin/agregar_video.html")
    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        file = request.files["file"]

        if file.filename == "":
            flash("Seleccione un archivo!")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_video = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)

            file.save(path_video)

            upload_result = upload_large(f"{path_video}",
                                        chunk_size = 500000000,
                                        folder = "rematescostarica/videos",
                                        resource_type = "video")
            os.remove(path_video)

            public_id = upload_result["public_id"]
            url_video = upload_result["secure_url"]
            filename_video = filename

            new_video = Videos(title=title, description=description, public_id=public_id, \
                              url_video=url_video, path_video=path_video, filename_video=filename_video)

            db.session.add(new_video)
            db.session.commit()

            return redirect(url_for("usuario_admin"))
        else:
            flash("Tipo de archivo no permitido!")
            return redirect(request.url)

@app.route("/perfil/usuario_admin/editar_video/<int:video_id>", methods=["GET", "POST"])
@login_required
def editar_video(video_id):
    """ Ruta para editar la informacion de cada video """
    pass

@app.route("/perfil/usuario_admin/eliminar_video/<int:video_id>", methods=["GET"])
@login_required
def eliminar_video(video_id):
    pass

@app.route("/perfil/usuario_admin/editar_perfil", methods=["GET", "POST"])
@login_required
def editar_perfil_admin():
    """ Ruta para poder editar el perfil del usuario admin """
    if request.method == "GET":
        username = session.get("username")

        if username != os.getenv("ADMIN_USERNAME"):
            return redirect(url_for("perfil", username=username))
        else:
            admin_user = Admin.query.filter_by(username=username).first()

            return render_template("admin/editar_perfil_admin.html", admin_user=admin_user)
    elif request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email_adress = request.form["email_adress"]
        password_value = request.form["password"]

        username = session.get("username")

        admin_user = Admin.query.filter_by(username=username).first()
        videos = Videos.query.all()
        users = Users.query.all()

        total_users = 0
        payment_completed_users = 0
        payment_uncompleted_users = 0

        for user in users:
            total_users = total_users + 1

            if user.payment_completed == "Sin Adquirir":
                payment_uncompleted_users = payment_uncompleted_users + 1

            if user.payment_completed == "Adquirido":
                payment_completed_users = payment_completed_users + 1

        total_data_info = {
            "total_users": total_users,
            "payment_completed_users": payment_completed_users,
            "payment_uncompleted_users": payment_uncompleted_users,
        }

        if password_value == "" or password_value == " ":
            admin_user.firstname = firstname
            admin_user.lastname = lastname
            admin_user.email_adress = email_adress
        else:
            admin_user.firstname = firstname
            admin_user.lastname = lastname
            admin_user.email_adress = email_adress
            password = generate_password_hash(password_value)
            admin_user.password = password

        db.session.add(admin_user)
        db.session.commit()

        return render_template("admin/usuario_admin.html", admin_user=admin_user, videos=videos, users=users, \
                               total_data_info=total_data_info)

@app.route("/create_file", methods=["GET"])
def create_file():
    """ Crear archivo excel con los datos de los usuarios """
    users = Users.query.all()
    wb = Workbook()
    user_array = []

    hoja = wb.active
    hoja.title = "Registro de usuarios"

    for user in users:
        user_array.append((
            user.firstname,
            user.lastname,
            user.username,
            user.phonenumber,
            user.email_adress,
            user.adress,
            user.postal_code,
            user.payment_completed
        ))

    hoja.append(("PrimerNombre", "PrimerApellido", "NombreDeUsuario", "NumeroTelefonico", \
                 "DireccionDeCorreo", "Direccion", "CodigoPostal", "EstadoDelCurso"))

    for item in user_array:
        hoja.append(item)

    wb.save("flaskr/static/files/Usuarios.xlsx")

    return jsonify({"message": "Creating file..."})
