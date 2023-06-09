from flask import flash, request, jsonify, redirect, render_template, url_for
from sqlalchemy.exc import NoResultFound
from flaskr import db
from flask_login import current_user, login_required
from flaskr.admin.base import bp
from flaskr.admin.forms import AddUpdateStudent
from flaskr.auth.email import send_user_information_email
from flaskr.helpers import generate_code

from flaskr.models.course import Course
from flaskr.models.person import Person
from flaskr.models.student_course import student_course
from flaskr.models.student import Student


@bp.route("/usuarios", methods=["GET", "POST"])
@login_required
def usuarios():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateStudent()

    users_count = Student.query.count()

    courses = db.session.execute(
        db.select(Course.course_name).order_by(Course.id)
    ).scalars()

    form.course.choices = [name for name in courses]

    if form.validate_on_submit():
        firstname = form.firstname.data
        first_lastname = form.first_lastname.data
        second_lastname = form.second_lastname.data
        email = form.email.data
        phone_number = form.phone_number.data
        course = form.course.data

        password = generate_code()
        student_code = generate_code()

        course = db.session.execute(
            db.select(Course).filter_by(course_name=course)
        ).scalar_one()

        person = Person(
            firstname=firstname,
            first_lastname=first_lastname,
            second_lastname=second_lastname,
            email=email,
        )

        person.is_admin = False
        person.set_password(password)

        student = Student(
            phone_number=phone_number,
            student_code=student_code,
            person=person,
        )

        student.is_active = True
        student.courses.append(course)

        db.session.add(person)
        db.session.add(student)
        db.session.commit()

        send_user_information_email(email=email, password=password)

        flash("Usuario agregado exitosamente!", "success")

        return redirect(url_for("admin.usuarios"))

    return render_template(
        "admin/usuarios.html",
        page="Usuarios",
        title="Usuarios",
        users_count=users_count,
        form=form,
    )


@bp.route("/usuarios/estado/<user_id>", methods=["GET"])
@login_required
def usuarios_estado(user_id):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    try:
        user = db.session.execute(
            db.select(Student).filter_by(id=user_id),
        ).scalar_one()

        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True

        db.session.add(user)
        db.session.commit()

        flash("Estado del usuario actualizado exitosamente!", "success")
    except NoResultFound:
        flash("Usuario no encontrado!", "error")

    return redirect(url_for("admin.usuarios"))


@bp.route("/usuarios/data", methods=["GET"])
@login_required
def usuarios_data():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    users_items = []
    total = 0

    users = db.session.execute(
        db.select(
            Person.firstname,
            Person.first_lastname,
            Person.second_lastname,
            Person.email,
            Student.id,
            Student.phone_number,
            Student.joined_in,
            Student.is_active,
            Course.course_name,
        )
        .select_from(Person)
        .join(Student)
        .join(student_course)
        .join(Course)
    )

    search = request.args.get("search")

    if search:
        users = db.session.execute(
            db.select(
                Person.firstname,
                Person.first_lastname,
                Person.second_lastname,
                Person.email,
                Student.id,
                Student.phone_number,
                Student.joined_in,
                Student.is_active,
                Course.course_name,
            )
            .select_from(Person)
            .join(Student)
            .join(student_course)
            .join(Course)
            .filter(
                db.or_(
                    Person.firstname.like(f"%{search}%"),
                    Person.email.like(f"%{search}%"),
                    Course.course_name.like(f"%{search}%"),
                )
            )
        )

    for u in users:
        users_items.append(
            {
                "firstname": u.firstname,
                "firstLastname": u.first_lastname,
                "secondLastname": u.second_lastname,
                "email": u.email,
                "phoneNumber": u.phone_number,
                "courseName": u.course_name,
                "joinedIn": u.joined_in,
                "isActive": u.is_active,
                "userId": u.id,
            }
        )

        total += 1

    return jsonify({"total": total, "data": users_items})
