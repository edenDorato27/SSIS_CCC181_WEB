from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, ValidationError
from flask_wtf.file import FileField, FileAllowed


class StudentForm(FlaskForm):
    id_number = StringField('id_number ', [validators.DataRequired(), validators.Length(min=9, max=20)])
    first_name = StringField('first_name', [validators.Length(min=3, max=50)])
    last_name = StringField('last_name', [validators.Length(min=2, max=50)])
    course_code = StringField('course_code', [validators.Length(min=3, max=50)])
    year_ = StringField('year_', [validators.Length(min=1, max=50)])
    gender = StringField('gender', [validators.Length(min=4, max=50)])
    profile_pic = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG and PNG images are allowed!')
    ], render_kw={'accept': 'image/*'})
    submit = SubmitField("Submit")

    def validate_id_number(form, field):
        id_number = field.data

        # Check if the ID number has the correct format (e.g., 1234-5678)
        if not (len(id_number) == 9 and id_number[:4].isdigit() and id_number[4] == '-' and id_number[5:].isdigit()):
            raise ValidationError('ID Number should follow this format "XXXX-XXXX".The X being a number.')