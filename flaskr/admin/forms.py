import phonenumbers
from flask_ckeditor import CKEditorField
from sqlalchemy.exc import NoResultFound
from flaskr import db
from flask_ckeditor.fields import TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import Email, InputRequired, Length, ValidationError
from wtforms import (
    FileField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TelField,
)

from flaskr.models.person import Person


class AddUpdateMaterial(FlaskForm):
    material_file = FileField("material_file", validators=[InputRequired()])
    submit = SubmitField("Agregar")


class AddUpdateVideo(FlaskForm):
    video_name = StringField(
        "video_name",
        validators=[
            InputRequired(),
            Length(max=160),
        ],
    )
    video_url = StringField(
        "video_url",
        validators=[
            InputRequired(),
            Length(max=300),
        ],
    )
    video_desc = CKEditorField("video_desc", validators=[Length(max=600)])
    submit = SubmitField("Agregar")


class AddUpdateCycle(FlaskForm):
    cycle_name = StringField(
        "cycle_name",
        validators=[
            InputRequired(),
            Length(max=160),
        ],
    )
    cycle_desc = TextAreaField("cycle_desc", validators=[Length(max=600)])
    submit = SubmitField("Agregar")


class AddUpdateStudent(FlaskForm):
    firstname = StringField(
        "firstname",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
    )
    first_lastname = StringField(
        "first_lastname",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
    )
    second_lastname = StringField(
        "second_lastname",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
    )
    email = StringField(
        "email",
        validators=[
            InputRequired(),
            Length(max=280),
            Email(message="Correo electrónico no válido!"),
        ],
    )
    phone_number = TelField("Telefono", validators=[InputRequired()])
    course = SelectField("course", choices=[])
    submit = SubmitField("Agregar")

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


class AddUpdateCourse(FlaskForm):
    course_name = StringField(
        "course_name",
        validators=[
            InputRequired(),
            Length(max=160),
        ],
    )
    course_basic_desc = TextAreaField(
        "course_basic_desc",
        validators=[
            Length(max=600),
        ],
    )
    course_desc = CKEditorField("course_desc", validators=[Length(max=600)])
    course_price = StringField("course_price", validators=[InputRequired()])
    course_image = FileField("course_image")
    submit = SubmitField("Agregar")


class AddUpdateChange(FlaskForm):
    change_price = StringField("course_price", validators=[InputRequired()])
    submit = SubmitField("Actualizar")


class UpdatePassword(FlaskForm):
    password = PasswordField(
        "password",
        validators=[
            InputRequired(),
            Length(min=8),
        ],
    )
    submit = SubmitField("Actualizar")
