from flask import redirect, render_template, url_for
from flaskr import db
from flask_login import current_user, login_required
from flaskr.models.cycle import Cycle
from flaskr.models.video import Video
from flaskr.user.base import bp

from flaskr.models.student_course import student_course
from flaskr.models.course import Course
from flaskr.models.student import Student


@bp.route("/dashboard/<student_code>", methods=["GET"])
@login_required
def dashboard(student_code):
    student = db.session.execute(
        db.select(Student).filter_by(student_code=student_code)
    ).scalar_one()

    if current_user.id != student.person_id:
        return redirect(
            url_for(
                "user.dashboard",
                student_code=student_code,
            )
        )

    videos = []

    course = db.session.execute(
        db.select(Course)
        .join(student_course)
        .filter(student_course.c.student_id == student.id)
    ).scalar_one()

    cycles = (
        db.session.execute(
            db.select(Cycle).filter(
                Cycle.course_id == course.id,
            )
        )
        .scalars()
        .all()
    )

    for cycle in cycles:
        videos_db = (
            db.session.execute(
                db.select(Video).filter(Video.cycle_id == cycle.id),
            )
            .scalars()
            .all()
        )

        for video in videos_db:
            videos.append(video)

    return render_template(
        "user/index.html",
        page="Dashboard",
        title="Dashboard",
        course=course,
        videos=videos,
        student_code=student_code,
    )


@bp.route("/dashboard/<student_code>/video/<video_code>", methods=["GET"])
@login_required
def dashboard_video(student_code, video_code):
    student = db.session.execute(
        db.select(Student).filter_by(student_code=student_code)
    ).scalar_one()

    if current_user.id != student.person_id:
        return redirect(
            url_for(
                "user.dashboard",
                student_code=student_code,
            )
        )

    videos = []

    course = db.session.execute(
        db.select(Course)
        .join(student_course)
        .filter(student_course.c.student_id == student.id)
    ).scalar_one()

    cycles = (
        db.session.execute(
            db.select(Cycle).filter(
                Cycle.course_id == course.id,
            )
        )
        .scalars()
        .all()
    )

    current_video = db.session.execute(
        db.select(Video).filter_by(video_code=video_code)
    ).scalar_one()

    for cycle in cycles:
        videos_db = (
            db.session.execute(
                db.select(Video).filter(Video.cycle_id == cycle.id),
            )
            .scalars()
            .all()
        )

        for video in videos_db:
            videos.append(video)

    return render_template(
        "user/video.html",
        page="Dashboard",
        title="Dashboard",
        current_video=current_video,
        course=course,
        videos=videos,
        student_code=student_code,
    )
