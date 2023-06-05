from flask import redirect, render_template, url_for
from flask_login import current_user, login_required
from flaskr.admin.base import bp


@bp.route("/usuarios", methods=["GET"])
@login_required
def usuarios():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    return render_template(
        "admin/usuarios.html",
        page="Usuarios",
        title="Usuarios",
    )
