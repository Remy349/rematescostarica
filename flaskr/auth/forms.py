import phonenumbers
from sqlalchemy.exc import NoResultFound
from flaskr import db
from flask_wtf import FlaskForm
from wtforms.validators import Email, InputRequired, Length, ValidationError
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TelField,
)

from flaskr.models.person import Person


class IngresarForm(FlaskForm):
    email = StringField("Correo", validators=[InputRequired()])
    password = PasswordField("Contraseña", validators=[InputRequired()])
    remember_me = BooleanField("Recordar sesión")
    submit = SubmitField("Iniciar sesión")


class RegistroForm(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
    )
    first_lastname = StringField(
        "Primer Apellido",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
    )
    second_lastname = StringField(
        "Segundo Apellido",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
    )
    email = StringField(
        "Correo",
        validators=[
            InputRequired(),
            Length(max=280),
            Email(message="Correo electrónico no válido!"),
        ],
    )
    phone_number = TelField("Telefono", validators=[InputRequired()])
    submit = SubmitField("Confirmar")

    def validate_email(self, email):
        try:
            user = db.session.execute(
                db.select(Person).filter_by(email=email.data)
            ).scalar_one()

            if user is not None:
                raise ValidationError("Correo electrónico ya registrado!")
        except NoResultFound:
            pass

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)

            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError("Número de teléfono no válido")
