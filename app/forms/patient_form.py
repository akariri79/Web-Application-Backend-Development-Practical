from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField
from wtforms.validators import DataRequired, Length


class PatientForm(FlaskForm):
    patient_id = StringField("Patient ID", validators=[DataRequired(), Length(max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    # middle_name = StringField('Middle Name (Optional)', validators=[Optional()])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    gender = RadioField('Gender', choices=[('Male', 'Male'),('Female', 'Female')],validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    registration_date = DateField(
        'Registration Date',
        default=date.today,
        format='%Y-%m-%d'
    )
    submit = SubmitField('Submit')