from flask import flash, redirect, render_template, request
from flaskr import db
from flask_ckeditor import url_for
from flask_login import current_user, login_required
from flaskr.admin.base import bp
from flaskr.admin.forms import AddUpdateFaq

from flaskr.models.faq import Faq


@bp.route("/editar-pagina", methods=["GET"])
@login_required
def editar_pagina():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    faqs = db.session.execute(db.select(Faq)).scalars().all()

    return render_template(
        "admin/editar-pagina.html",
        page="Editar Página",
        title="Editar Página",
        faqs=faqs,
    )


@bp.route("/editar-pagina/agregar-faq", methods=["GET", "POST"])
@login_required
def editar_pagina_agregar_faq():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateFaq()

    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data

        faq = Faq(question=question, answer=answer)

        db.session.add(faq)
        db.session.commit()

        flash("Faq agregado exitosamente!", "success")

        return redirect(url_for("admin.editar_pagina_agregar_faq"))

    return render_template(
        "admin/editar/agregar-faq.html",
        page="Editar Página",
        title="Editar Página",
        form=form,
    )


@bp.route("/editar-pagina/editar-faq/<faq_id>", methods=["GET", "POST"])
@login_required
def editar_pagina_editar_faq(faq_id):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateFaq()

    faq = db.session.execute(
        db.select(Faq).filter(Faq.id == faq_id),
    ).scalar_one()

    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data

        faq.question = question
        faq.answer = answer

        db.session.add(faq)
        db.session.commit()

        flash("Faq actualizado exitosamente!", "success")

        return redirect(url_for("admin.editar_pagina"))
    elif request.method == "GET":
        form.question.data = faq.question
        form.answer.data = faq.answer

    return render_template(
        "admin/editar/editar-faq.html",
        page="Editar Página",
        title="Editar Página",
        form=form,
    )


@bp.route("/editar-pagina/eliminar-faq/<faq_id>", methods=["GET"])
@login_required
def editar_pagina_eliminar_faq(faq_id):
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    faq = db.get_or_404(Faq, faq_id)

    db.session.delete(faq)
    db.session.commit()

    flash("Faq eliminado exitosamente!", "success")

    return redirect(url_for("admin.editar_pagina"))
