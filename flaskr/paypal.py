from flaskr import app, db
from flask import jsonify, request, session

from flaskr.models import Registro, Users


@app.route("/payment-completed", methods=["POST"])
def payment_completed():
    data = request.get_json() or {}
    # email_adress = session.get("email_adress")
    user_id = session.get("user_id")

    # registro = Registro.query.filter_by(email_adress=email_adress).first()
    user = Users.query.filter_by(id=user_id).first()

    if data["success"] == "COMPLETED":
        payment_completed = "Adquirido"
        course_type = data["course_type"]

        # registro.payment_completed = payment_completed
        user.payment_completed = payment_completed
        user.course_type = course_type

        # db.session.add(registro)
        # db.session.commit()

        db.session.add(user)
        db.session.commit()

        # session.pop("email_adress", None)

    return jsonify({"message": "SUCCESS"})
