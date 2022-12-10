from flaskr import app, db
from flask import jsonify, request, session

from flaskr.models import Registro


@app.route("/payment-completed", methods=["POST"])
def payment_completed():
    data = request.get_json() or {}
    email_adress = session.get("email_adress")

    registro = Registro.query.filter_by(email_adress=email_adress).first()

    if data["success"] == "COMPLETED":
        payment_completed = "Adquirido"

        registro.payment_completed = payment_completed

        db.session.add(registro)
        db.session.commit()

        session.clear()

    return jsonify({"message": "SUCCESS"})
