import os
from flask import redirect, request, session, url_for
from flaskr import app, db
from helpers import login_required

from flaskr.models import Posts, Admin

@app.route("/post/agregar", methods=["GET", "POST"])
@login_required
def agregar_post():
    """ Ruta/Funcion para manejar la creacion de publicaciones por parte del usuario admin """
    if request.method == "GET":
        return redirect(url_for("index"))
    elif request.method == "POST":
        username = os.getenv("ADMIN_USERNAME")

        title = None
        description = request.form["description"]
        admin_user = Admin.query.filter_by(username=username).first()
        user_image = f"http://www.gravatar.com/avatar/{admin_user.gravatar}?d=identicon"

        if request.form["title"] == "":
            title = "<--Sin titulo-->"
        else:
            title = request.form["title"]

        new_post = Posts(title=title, description=description, user_image=user_image)

        db.session.add(new_post)
        db.session.commit()

        print(new_post)

        return redirect(url_for("index"))

@app.route("/post/eliminar/<int:post_id>", methods=["GET"])
@login_required
def eliminar_post(post_id):
    """ Ruta/Funcion para eliminar los posts de la base de datos """
    username = session.get("username")

    if username != os.getenv("ADMIN_USERNAME"):
        return redirect(url_for("index"))
    else:
        delete_post = Posts.query.filter_by(id=post_id).first()
        
        db.session.delete(delete_post)
        db.session.commit()

        return redirect(url_for("index"))
