from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class StudentForm(FlaskForm):
    id_number = StringField('id_number ', [validators.DataRequired(), validators.Length(min=9, max=20)])
    first_name = StringField('first_name', [validators.Length(min=3, max=50)])
    last_name = StringField('last_name', [validators.Length(min=2, max=50)])
    course_code = StringField('course_code', [validators.Length(min=3, max=50)])
    year_ = StringField('year_', [validators.Length(min=1, max=50)])
    gender = StringField('gender', [validators.Length(min=4, max=50)])
    submit = SubmitField("Submit")
