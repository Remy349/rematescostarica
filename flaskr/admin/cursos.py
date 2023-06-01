from flask import flash, redirect, render_template, url_for
from cloudinary.uploader import upload
from flaskr import db
from flask_login import current_user, login_required
from flaskr.admin.base import bp
from flaskr.admin.forms import AddUpdateCourse
from flaskr.helpers import allowed_file, generate_code

from flaskr.models.course import Course


@bp.route("/cursos", methods=["GET"])
@login_required
def cursos():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    courses = db.session.execute(db.select(Course)).scalars().all()

    return render_template(
        "admin/cursos.html",
        page="Cursos",
        title="Cursos",
        courses=courses,
    )


@bp.route("/cursos/agregar-curso", methods=["GET", "POST"])
@login_required
def cursos_agregar_curso():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateCourse()

    if form.validate_on_submit():
        course_name = form.course_name.data
        course_desc = form.course_desc.data
        course_price = form.course_price.data
        course_image = form.course_image.data

        course_code = generate_code()

        course = Course(
            course_name=course_name,
            course_price=course_price,
            course_desc=course_desc,
            course_code=course_code,
        )

        if course_image.filename == "":
            flash("No se ha seleccionado ningún archivo!", "error")
            return redirect(url_for("admin.cursos_agregar_curso"))

        if course_image and allowed_file(course_image.filename):
            upload_result = upload(
                course_image,
                resource_type="image",
                folder="/rematescostarica",
            )

            secure_url = upload_result["secure_url"]
            public_id = upload_result["public_id"]

            course.secure_url = secure_url
            course.public_id = public_id
        else:
            flash("Tipo de archivo no permitido!", "error")
            return redirect(url_for("admin.cursos_agregar_curso"))

        db.session.add(course)
        db.session.commit()

        flash("Curso agregado exitosamente!", "success")

        return redirect(url_for("admin.cursos"))

    return render_template(
        "admin/cursos/agregar-curso.html",
        form=form,
        title="Agregar curso",
        page="Agregar curso",
    )