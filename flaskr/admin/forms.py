from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import InputRequired, Length


class AddUpdateCourse(FlaskForm):
    course_name = StringField("course_name", validators=[InputRequired(), Length(max=160)])
    course_desc = CKEditorField("course_desc", validators=[Length(max=600)])
    course_price = StringField("course_price", validators=[InputRequired()])
    course_image = FileField("course_image")
    submit = SubmitField("Agregar")


class AddUpdateChange(FlaskForm):
    change_price = StringField("course_price", validators=[InputRequired()])
    submit = SubmitField("Actualizar")
