from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class CollegeForm(FlaskForm):
    college_code = StringField('college_code ', [validators.DataRequired(), validators.Length(min=3, max=20)])
    college_name = StringField('college_name', [validators.Length(min=3, max=50)])
    submit = SubmitField("Submit")
