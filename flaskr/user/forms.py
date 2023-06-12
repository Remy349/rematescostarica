from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class UpdatePassword(FlaskForm):
    password = PasswordField(
        "password",
        validators=[
            InputRequired(),
            Length(min=8),
        ],
    )
    submit = SubmitField("Actualizar")
