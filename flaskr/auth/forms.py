from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TelField
from wtforms.validators import InputRequired


class IngresarForm(FlaskForm):
    email = StringField("Correo", validators=[InputRequired()])
    password = PasswordField("Contraseña", validators=[InputRequired()])
    remember_me = BooleanField("Recordar sesión")
    submit = SubmitField("Iniciar sesión")


class RegistroForm(FlaskForm):
    firstname = StringField("Nombre", validators=[InputRequired()])
    first_lastname = StringField("Primer Apellido", validators=[InputRequired()])
    second_lastname = StringField("Segundo Apellido", validators=[InputRequired()])
    email = StringField("Correo", validators=[InputRequired()])
    phone_number = TelField("Telefono", validators=[InputRequired()])
    submit = SubmitField("Comprar")
