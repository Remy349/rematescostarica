from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class IngresarForm(FlaskForm):
    email = StringField("Correo", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recordar sesión")
    submit = SubmitField("Iniciar sesión")
