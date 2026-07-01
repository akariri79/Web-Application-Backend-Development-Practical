from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange

class VitalsForm(FlaskForm):
    # visit_date = DateField('Visit Date', format='%Y-%m-%d', validators=[DataRequired()])
    height_cm = FloatField('Height (cm)', validators=[DataRequired(), NumberRange(min=20, max=210)])
    weight_kg = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=1, max=500)])
    submit = SubmitField('Submit')