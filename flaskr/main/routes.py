from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")
