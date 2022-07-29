import os
from werkzeug.utils import secure_filename
from flaskr import app, db
from flask import flash, redirect, request, session, url_for
from helpers import login_required

from flaskr.models import ContentPage, Images

ALLOWED_EXTENSIONS = {"png", "gif", "jpg", "svg", "jpeg"}

def allowed_file(filename):
    """ Funcion para validar la extension de los archivos a subir """
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/contenido/agregar", methods=["GET", "POST"])
@login_required
def agregar_contenido():
    """ Funcion/Ruta para agregar contenido nuevo a cada pagina del sitio """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        if request.method == "GET":
            return redirect(url_for("index"))
        elif request.method == "POST":
            information_content = request.form["information_content"]
            from_page = request.form["from_page"]
            from_section = request.form["from_section"]

            redirect_page = None

            new_content_page = ContentPage(information_content=information_content, \
                    from_page=from_page, from_section=from_section)

            db.session.add(new_content_page)
            db.session.commit()

            if from_page == "home":
                redirect_page = "index"
            elif from_page == "quienes_somos":
                redirect_page = "quienes_somos"

            if session.get("is_edit") and session.get("is_edit_id") is None:
                pass
            else:
                session.pop("is_edit", None)
                session.pop("is_edit_id", None)

            return redirect(url_for(f"{redirect_page}"))

@app.route("/contenido/editar/<int:content_page_id>", methods=["GET", "POST"])
@login_required
def editar_contenido(content_page_id):
    """ Ruta/Funcion para editar el contenido de cada pagina del sitio """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        if request.method == "GET":
            if session.get("is_edit") and session.get("is_edit_id") is None:
                session["is_edit"] = "true"
                session["is_edit_id"] = content_page_id
            else:
                session.pop("is_edit", None)
                session.pop("is_edit_id", None)

                session["is_edit"] = "true"
                session["is_edit_id"] = content_page_id

            edit_content_page = ContentPage.query.filter_by(id=content_page_id).first()

            redirect_page = None

            if edit_content_page.from_page == "home":
                redirect_page = "index"
            elif edit_content_page.from_page == "quienes_somos":
                redirect_page = "quienes_somos"

            return redirect(url_for(f"{redirect_page}"))
        elif request.method == "POST":
            information_content = request.form["information_content"]

            edit_content_page = ContentPage.query.filter_by(id=content_page_id).first()

            redirect_page = None

            if edit_content_page.from_page == "home":
                redirect_page = "index"
            elif edit_content_page.from_page == "quienes_somos":
                redirect_page = "quienes_somos"

            edit_content_page.information_content = information_content

            db.session.add(edit_content_page)
            db.session.commit()

            session.pop("is_edit", None)
            session.pop("is_edit_id", None)

            return redirect(url_for(f"{redirect_page}"))

@app.route("/contenido/cancelar/<int:content_page_id>", methods=["GET"])
@login_required
def cancelar_contenido(content_page_id):
    """ Ruta/Funcion para cancelar el proceso de edicion de contenido """
    cancel_content_page = ContentPage.query.filter_by(id=content_page_id).first()

    redirect_page = None

    if cancel_content_page.from_page == "home":
        redirect_page = "index"
    elif cancel_content_page.from_page == "quienes_somos":
        redirect_page = "quienes_somos"

    session.pop("is_edit", None)
    session.pop("is_edit_id", None)

    return redirect(url_for(f"{redirect_page}"))

@app.route("/contenido/eliminar/<int:content_page_id>", methods=["GET"])
@login_required
def eliminar_contenido(content_page_id):
    """ Ruta/Funcion para eliminar el contenido de cada pagina del sitio """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        redirect_page = None
        delete_content_page = ContentPage.query.filter_by(id=content_page_id).first()

        if delete_content_page.from_page == "home":
            redirect_page = "index"
        elif delete_content_page.from_page == "quienes_somos":
            redirect_page = "quienes_somos"

        db.session.delete(delete_content_page)
        db.session.commit()

        if session.get("is_edit") and session.get("is_edit_id") is None:
            pass
        else:
            session.pop("is_edit", None)
            session.pop("is_edit_id", None)

        return redirect(url_for(f"{redirect_page}"))

@app.route("/contenido/imagen/agregar", methods=["GET", "POST"])
@login_required
def agregar_imagen_contenido():
    """ Ruta/Funcion para agregar imagenes a la pagina principal """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        if request.method == "GET":
            return redirect(url_for("index"))
        elif request.method == "POST":
            file = request.files["file"]
            from_page = request.form["from_page"]
            from_section = request.form["from_section"]
            
            if file.filename == "":
                flash("Seleccione un archivo!")
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path_image = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
                relative_path_image = f"static/img/{filename}"

                file.save(path_image)

                new_image = Images(path_image=path_image, filename_image=filename, from_page=from_page, \
                        from_section=from_section, relative_path_image=relative_path_image)

                db.session.add(new_image)
                db.session.commit()

                return redirect(url_for("index"))
            else:
                flash("Tipo de archivo no permitido!")
                return redirect(request.url)

@app.route("/contenido/imagen/editar/<int:image_page_id>", methods=["GET", "POST"])
@login_required
def editar_imagen_contenido(image_page_id):
    """ Ruta/Funcion para editar las imagenes del home """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        if request.method == "GET":
            return redirect(url_for("index"))
        elif request.method == "POST":
            file = request.files["file"]
            from_page = request.form["from_page"]
            from_section = request.form["from_section"]

            if file.filename == "":
                flash("Seleccione un archivo!")
                return redirect(request.url)

            if file and allowed_file(file.filename):
                edit_image = Images.query.filter_by(id=image_page_id).first()

                os.remove(edit_image.path_image)

                filename = secure_filename(file.filename)
                path_image = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
                relative_path_image = f"static/img/{filename}"

                file.save(path_image)

                edit_image.path_image = path_image
                edit_image.filename_image = filename
                edit_image.from_page = from_page
                edit_image.from_section = from_section
                edit_image.relative_path_image = relative_path_image

                db.session.add(edit_image)
                db.session.commit()

                return redirect(url_for("index"))
            else:
                flash("Tipo de archivo no permitido!")
                return redirect(request.url)

@app.route("/contenido/imagen/eliminar/<int:image_page_id>", methods=["GET"])
@login_required
def eliminar_imagen_contenido(image_page_id):
    """ Ruta/Funcion para eliminar la imagen de la pagina home """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        delete_image = Images.query.filter_by(id=image_page_id).first()

        os.remove(delete_image.path_image)

        db.session.delete(delete_image)
        db.session.commit()

        return redirect(url_for("index"))
