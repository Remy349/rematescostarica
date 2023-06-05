from flask import flash, jsonify, redirect, request, render_template, url_for
from sqlalchemy.exc import StatementError
from flaskr import db
from flask_login import current_user, login_required
from flaskr.admin.base import bp
from flaskr.admin.forms import AddUpdateChange

from flaskr.models.change import Change
from flaskr.models.course import Course
from flaskr.models.person import Person
from flaskr.models.purchase_paypal import PurchasePaypal
from flaskr.models.student import Student


@bp.route("/pagos", methods=["GET", "POST"])
@login_required
def pagos():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateChange()

    paypal_net_amount = sum(
        db.session.execute(db.select(PurchasePaypal.purchase_net_amount))
        .scalars()
        .all()
    )

    change = db.session.execute(db.select(Change)).scalar_one()

    if form.validate_on_submit():
        try:
            change_price = form.change_price.data

            change.change_price = change_price

            db.session.add(change)
            db.session.commit()

            flash(f"Nuevo tipo de cambio: {change_price}", "success")
        except StatementError:
            flash("No se permiten letras para el tipo de cambio!", "error")

        return redirect(url_for("admin.pagos"))
    elif request.method == "GET":
        form.change_price.data = change.change_price

    return render_template(
        "admin/pagos.html",
        page="Pagos",
        title="Pagos",
        paypal_net_amount=paypal_net_amount,
        form=form,
        change=change,
    )


@bp.route("/pagos/paypal/data", methods=["GET"])
@login_required
def pagos_data():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    purchases_paypal_items = []
    total = 0

    purchases_paypal = db.session.execute(
        db.select(
            Person.firstname,
            Person.first_lastname,
            Person.second_lastname,
            Person.email,
            Course.course_name,
            PurchasePaypal.purchase_gross_amount,
            PurchasePaypal.purchase_paypal_fee,
            PurchasePaypal.purchase_net_amount,
            PurchasePaypal.purchase_date,
        )
        .select_from(PurchasePaypal)
        .join(Student)
        .join(Person)
        .join(Course)
    )

    for purchase in purchases_paypal:
        purchases_paypal_items.append(
            {
                "firstname": purchase.firstname,
                "firstLastname": purchase.first_lastname,
                "secondLastname": purchase.second_lastname,
                "email": purchase.email,
                "courseName": purchase.course_name,
                "grossAmount": purchase.purchase_gross_amount,
                "paypalFee": purchase.purchase_paypal_fee,
                "netAmount": purchase.purchase_net_amount,
                "date": purchase.purchase_date,
            }
        )

        total += 1

    return jsonify({"total": total, "data": purchases_paypal_items})
