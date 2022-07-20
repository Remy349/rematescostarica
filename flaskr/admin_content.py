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

        new_content_page = ContentPage(information_content=information_content, \
                from_page=from_page, from_section=from_section)

        db.session.add(new_content_page)
        db.session.commit()

        return redirect(url_for("index"))

@app.route("/contenido/eliminar/<int:content_page_id>", methods=["GET"])
@login_required
def eliminar_contenido(content_page_id):
    """ Ruta/Funcion para eliminar el contenido de cada pagina del sitio """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        delete_content_page = ContentPage.query.filter_by(id=content_page_id).first()
        
        db.session.delete(delete_content_page)
        db.session.commit()

        return redirect(url_for("index"))
