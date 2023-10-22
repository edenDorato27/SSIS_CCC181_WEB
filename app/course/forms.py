from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class CourseForm(FlaskForm):
    course_code = StringField('course_code ', [validators.DataRequired(), validators.Length(min=1, max=20)])
    course_name = StringField('course_name', [validators.Length(min=1, max=50)])
    college_code = StringField('college_code', [validators.Length(min=1, max=50)])
    submit = SubmitField("Submit")
