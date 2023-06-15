from flask import current_app, render_template
from flaskr.email import send_email


def send_user_information_email(email, password):
    user_info = {"email": email, "password": password}

    send_email(
        "[Remates Costa Rica] Información de usuario",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[email],
        text_body=render_template(
            "auth/email/user-info.txt",
            user_info=user_info,
        ),
        text_html=render_template(
            "auth/email/user-info.html",
            user_info=user_info,
        ),
    )


def send_password_reset_email(user):
    token = user.get_reset_password_token()

    send_email(
        "[Remates Costa Rica] Cambia tu contraseña",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
        text_body=render_template(
            "auth/email/reset-password.txt",
            user=user,
            token=token,
        ),
        text_html=render_template(
            "auth/email/reset-password.html",
            user=user,
            token=token,
        ),
    )
