from flask import jsonify, redirect, render_template, url_for
from flaskr import db
from flask_login import current_user, login_required
from flaskr.admin.base import bp
from sqlalchemy import func

from flaskr.models.course import Course
from flaskr.models.purchase_paypal import PurchasePaypal
from flaskr.models.student import Student
from flaskr.models.student_course import student_course


@bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    data_stats = {}

    users_course = []

    courses = db.session.execute(db.select(Course).limit(2)).scalars().all()

    paypal_net_amount = (
        db.session.execute(db.select(PurchasePaypal.purchase_net_amount))
        .scalars()
        .all()
    )

    data_stats["total_users"] = Student.query.count()
    data_stats["paypal_net_amount"] = sum(paypal_net_amount)

    for course in courses:
        users_count = (
            db.session.query(func.count(student_course.c.student_id))
            .filter(student_course.c.course_id == course.id)
            .scalar()
        )

        user_data = {
            "course_name": course.course_name,
            "users_count": users_count,
        }

        users_course.append(user_data)

    return render_template(
        "admin/index.html",
        page="Dashboard",
        title="Dashboard",
        data_stats=data_stats,
        users_course=users_course,
    )


@bp.route("/dashboard/data", methods=["GET"])
@login_required
def dashboard_data():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    data_charts = {}
    pie_chart = {}
    line_chart = {}

    users = []
    line_labels = []
    line_data = []

    courses = db.session.execute(db.select(Course)).scalars().all()

    purchases_paypal = db.session.execute(
        db.select(
            PurchasePaypal.purchase_net_amount,
            PurchasePaypal.purchase_date,
        )
        .group_by(
            PurchasePaypal.purchase_date,
            PurchasePaypal.purchase_net_amount,
        )
        .order_by(PurchasePaypal.purchase_date)
    ).all()

    for amount, date in purchases_paypal:
        line_labels.append(date.strftime("%m-%d-%y"))
        line_data.append(amount)

    for course in courses:
        users_count = (
            db.session.query(func.count(student_course.c.student_id))
            .filter(student_course.c.course_id == course.id)
            .scalar()
        )

        users.append(users_count)

    pie_chart["labels"] = [course.course_name for course in courses]
    pie_chart["data"] = users

    line_chart["labels"] = line_labels
    line_chart["data"] = line_data

    data_charts["pie"] = pie_chart
    data_charts["line"] = line_chart

    return jsonify(data_charts)
