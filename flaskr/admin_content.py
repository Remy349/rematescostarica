from flask_session import os
from flaskr import app, db
from flask import redirect, request, session, url_for
from helpers import login_required

from flaskr.models import ContentPage

@app.route("/contenido/agregar", methods=["GET", "POST"])
@login_required
def agregar_contenido():
    """ Funcion/Ruta para agregar contenido nuevo a cada pagina del sitio """
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
