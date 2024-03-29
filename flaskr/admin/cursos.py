from cloudinary.uploader import upload
from sqlalchemy import func
from sqlalchemy.exc import StatementError
from flaskr import db
from flask_login import current_user, login_required
from flaskr.admin.base import bp
from flaskr.helpers import allowed_file, generate_code
from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from flaskr.admin.forms import (
    AddUpdateCourse,
    AddUpdateCycle,
    AddUpdateMaterial,
    AddUpdateVideo,
)

from flaskr.models.course import Course
from flaskr.models.cycle import Cycle
from flaskr.models.person import Person
from flaskr.models.student import Student
from flaskr.models.student_course import student_course
from flaskr.models.video import Video


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
        try:
            course_name = form.course_name.data
            course_basic_desc = form.course_basic_desc.data
            course_desc = form.course_desc.data
            course_price = form.course_price.data
            course_image = form.course_image.data

            course_code = generate_code()

            course = Course(
                course_name=course_name,
                course_price=course_price,
                course_basic_desc=course_basic_desc,
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
        except StatementError:
            flash("No se permiten letras para el precio del curso", "error")
            return redirect(url_for("admin.cursos_agregar_curso"))

        return redirect(url_for("admin.cursos"))

    return render_template(
        "admin/cursos/agregar-curso.html",
        form=form,
        title="Agregar curso",
        page="Agregar curso",
    )


@bp.route("/cursos/<course_code>", methods=["GET", "POST"])
@login_required
def cursos_control(course_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateCourse()

    course = db.session.execute(
        db.select(Course).filter_by(course_code=course_code)
    ).scalar_one()

    cycles = db.session.execute(
        db.select(
            Cycle.cycle_name,
            Cycle.cycle_desc,
            Cycle.cycle_code,
        ).filter(Cycle.course_id == course.id)
    ).all()

    users_count = (
        db.session.query(func.count(student_course.c.student_id))
        .filter(student_course.c.course_id == course.id)
        .scalar()
    )

    session.pop("course_code", None)
    session["course_code"] = course.course_code

    if form.validate_on_submit():
        try:
            course_name = form.course_name.data
            course_price = form.course_price.data
            course_basic_desc = form.course_basic_desc.data
            course_desc = form.course_desc.data
            course_image = form.course_image.data

            course.course_name = course_name
            course.course_price = course_price
            course.course_basic_desc = course_basic_desc
            course.course_desc = course_desc

            if course_image.filename == "":
                pass
            else:
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

                    return redirect(
                        url_for(
                            "admin.cursos_control",
                            course_code=course_code,
                        )
                    )

            db.session.add(course)
            db.session.commit()

            flash("Datos del curso actualizados exitosamente!", "success")
        except StatementError:
            flash("No se permiten letras para el precio del curso!", "error")

        return redirect(
            url_for(
                "admin.cursos_control",
                course_code=course_code,
            )
        )
    elif request.method == "GET":
        form.course_name.data = course.course_name
        form.course_price.data = course.course_price
        form.course_basic_desc.data = course.course_basic_desc
        form.course_desc.data = course.course_desc

    return render_template(
        "admin/cursos/cursos-control.html",
        page=f"Curso: {course.course_name}",
        title=f"Curso: {course.course_name}",
        course=course,
        form=form,
        users_count=users_count,
        cycles=cycles,
    )


@bp.route("/cursos/<course_code>/<cycle_code>", methods=["GET", "POST"])
@login_required
def cursos_ciclo(course_code, cycle_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateCycle()

    course = db.session.execute(
        db.select(Course).filter_by(course_code=course_code)
    ).scalar_one()

    cycle = db.session.execute(
        db.select(Cycle).filter(
            Cycle.cycle_code.like(cycle_code),
            Cycle.course_id == course.id,
        )
    ).scalar_one()

    videos = (
        db.session.execute(
            db.select(Video).filter(
                Video.cycle_id == cycle.id,
            )
        )
        .scalars()
        .all()
    )

    if form.validate_on_submit():
        cycle_name = form.cycle_name.data
        cycle_desc = form.cycle_desc.data

        cycle.cycle_name = cycle_name
        cycle.cycle_desc = cycle_desc

        db.session.add(cycle)
        db.session.commit()

        flash("Ciclo actualizado exitosamente!", "success")

        return redirect(
            url_for(
                "admin.cursos_ciclo",
                course_code=course_code,
                cycle_code=cycle_code,
            )
        )
    elif request.method == "GET":
        form.cycle_name.data = cycle.cycle_name
        form.cycle_desc.data = cycle.cycle_desc

    return render_template(
        "admin/cursos/ciclo.html",
        page=f"Curso: {course.course_name}",
        title=f"Curso: {course.course_name}",
        course=course,
        cycle=cycle,
        form=form,
        videos=videos,
    )


@bp.route(
    "/cursos/<course_code>/<cycle_code>/<video_code>",
    methods=["GET", "POST"],
)
@login_required
def cursos_ciclo_video(course_code, cycle_code, video_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    course = db.session.execute(
        db.select(Course).filter_by(course_code=course_code)
    ).scalar_one()

    cycle = db.session.execute(
        db.select(Cycle).filter(
            Cycle.cycle_code.like(cycle_code),
            Cycle.course_id == course.id,
        )
    ).scalar_one()

    current_video = db.session.execute(
        db.select(Video).filter(
            Video.cycle_id == cycle.id,
            Video.video_code.like(video_code),
        )
    ).scalar_one()

    videos = (
        db.session.execute(
            db.select(Video).filter(
                Video.cycle_id == cycle.id,
            )
        )
        .scalars()
        .all()
    )

    form = AddUpdateVideo()

    if form.validate_on_submit():
        video_name = form.video_name.data
        video_desc = form.video_desc.data

        current_video.video_name = video_name
        current_video.video_desc = video_desc

        db.session.add(current_video)
        db.session.commit()

        flash("Video actualizado exitosamente!", "success")

        return redirect(
            url_for(
                "admin.cursos_ciclo_video",
                course_code=course_code,
                cycle_code=cycle_code,
                video_code=video_code,
            )
        )
    elif request.method == "GET":
        form.video_name.data = current_video.video_name
        form.video_url.data = current_video.video_url
        form.video_desc.data = current_video.video_desc

    return render_template(
        "admin/cursos/ciclo-video.html",
        course=course,
        cycle=cycle,
        page=f"Curso: {course.course_name}",
        title=f"Curso: {course.course_name}",
        form=form,
        current_video=current_video,
        videos=videos,
    )


@bp.route(
    "/cursos/<course_code>/<cycle_code>/<video_code>/agregar-material",
    methods=["GET", "POST"],
)
@login_required
def cursos_ciclo_video_agregar_material(course_code, cycle_code, video_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    course = db.session.execute(
        db.select(Course).filter_by(course_code=course_code)
    ).scalar_one()

    form = AddUpdateMaterial()

    if form.validate_on_submit():
        material_file = form.material_file.data

        flash("Material agregado exitosamente!", "success")

        return redirect(
            url_for(
                "admin.cursos_ciclo_video",
                course_code=course_code,
                cycle_code=cycle_code,
                video_code=video_code,
            )
        )

    return render_template(
        "admin/cursos/agregar-material.html",
        form=form,
        page=f"Curso: {course.course_name}",
        title=f"Curso: {course.course_name}",
        course_code=course_code,
        cycle_code=cycle_code,
        video_code=video_code,
    )


@bp.route(
    "/cursos/<course_code>/<cycle_code>/<video_code>/eliminar",
    methods=["GET"],
)
@login_required
def cursos_ciclo_video_eliminar(course_code, cycle_code, video_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    video = db.session.execute(
        db.select(Video).filter_by(video_code=video_code)
    ).scalar_one()

    db.session.delete(video)
    db.session.commit()

    flash("Video eliminado exitosamente!", "success")

    return redirect(
        url_for(
            "admin.cursos_ciclo",
            course_code=course_code,
            cycle_code=cycle_code,
        )
    )


@bp.route(
    "/cursos/<course_code>/<cycle_code>/agregar-video",
    methods=["GET", "POST"],
)
@login_required
def cursos_agregar_video(course_code, cycle_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateVideo()

    course = db.session.execute(
        db.select(Course).filter_by(course_code=course_code)
    ).scalar_one()

    cycle = db.session.execute(
        db.select(Cycle).filter_by(cycle_code=cycle_code)
    ).scalar_one()

    if form.validate_on_submit():
        video_name = form.video_name.data
        video_url = form.video_url.data
        video_desc = form.video_desc.data

        video_code = generate_code()

        video = Video(
            video_name=video_name,
            video_url=video_url,
            video_desc=video_desc,
            video_code=video_code,
            cycle=cycle,
        )

        db.session.add(video)
        db.session.commit()

        flash("Video agregado exitosamente!", "success")

        return redirect(
            url_for(
                "admin.cursos_ciclo",
                course_code=course_code,
                cycle_code=cycle_code,
            )
        )

    return render_template(
        "admin/cursos/agregar-video.html",
        form=form,
        course=course,
        cycle=cycle,
        page=f"Curso: {course.course_name}",
        title=f"Curso: {course.course_name}",
    )


@bp.route("/cursos/<course_code>/<cycle_code>/eliminar", methods=["GET"])
@login_required
def cursos_ciclo_eliminar(course_code, cycle_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    cycle = db.session.execute(
        db.select(Cycle).filter_by(cycle_code=cycle_code)
    ).scalar_one()

    db.session.delete(cycle)
    db.session.commit()

    flash("Ciclo eliminado exitosamente!", "success")

    return redirect(
        url_for(
            "admin.cursos_control",
            course_code=course_code,
        )
    )


@bp.route("/cursos/<course_code>/agregar-ciclo", methods=["GET", "POST"])
@login_required
def cursos_agregar_ciclo(course_code):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateCycle()

    course = db.session.execute(
        db.select(Course).filter_by(course_code=course_code)
    ).scalar_one()

    if form.validate_on_submit():
        cycle_name = form.cycle_name.data
        cycle_desc = form.cycle_desc.data

        cycle_code = generate_code()

        cycle = Cycle(
            cycle_name=cycle_name,
            cycle_desc=cycle_desc,
            cycle_code=cycle_code,
            course=course,
        )

        db.session.add(cycle)
        db.session.commit()

        flash("Ciclo agregado exitosamente!", "success")

        return redirect(
            url_for(
                "admin.cursos_control",
                course_code=course_code,
            )
        )

    return render_template(
        "admin/cursos/agregar-ciclo.html",
        form=form,
        course=course,
        page=f"Curso: {course.course_name}",
        title=f"Curso: {course.course_name}",
    )


@bp.route("/cursos/data", methods=["GET"])
@login_required
def cursos_data():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    course_code = session.get("course_code")

    users_items = []
    total = 0

    course = db.session.execute(
        db.select(Course).filter_by(course_code=course_code)
    ).scalar_one()

    users = course.students

    search = request.args.get("search")

    if search:
        users = (
            db.session.execute(
                db.select(Student)
                .join(Person)
                .filter(
                    db.or_(
                        Person.firstname.like(f"%{search}%"),
                        Person.email.like(f"%{search}%"),
                    ),
                    Student.courses.any(id=course.id),
                )
            )
            .scalars()
            .all()
        )

    for u in users:
        person = u.person

        users_items.append(
            {
                "firstname": person.firstname,
                "firstLastname": person.first_lastname,
                "secondLastname": person.second_lastname,
                "email": person.email,
                "phoneNumber": u.phone_number,
                "joinedIn": u.joined_in,
                "isActive": u.is_active,
            }
        )

        total += 1

    return jsonify({"totel": total, "data": users_items})
