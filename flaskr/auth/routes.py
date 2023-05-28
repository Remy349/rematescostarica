from flask import Blueprint, render_template
from flaskr.auth.forms import IngresarForm

bp = Blueprint("auth", __name__)


@bp.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    form = IngresarForm()

    return render_template("auth/ingresar.html", form=form)
