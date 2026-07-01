from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length

# Overweight Assessment Form created using FlaskForm
class OverweightAssessmentForm(FlaskForm):
    general_health = RadioField("General Health", choices=[('Good', 'Good'),('Poor', 'Poor')],
                                validators=[DataRequired()])
    diet_history = RadioField('Have you ever been on diet to lose weight',
                              validators=[DataRequired()],
                      choices=[('Yes', 'Yes'), ('Yes', 'No')])
    comments = TextAreaField('Comments', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Submit')

# General Assessment Form created using FlaskForm
class GeneralAssessmentForm(FlaskForm):
    general_health = RadioField("General Health", validators=[DataRequired()],
                                choices=[('option 1', 'Good'), ('option 2', 'Poor')])
    drug_usage = RadioField('Are you currently using any drugs',
                            validators=[DataRequired()],
                            choices=[('Yes','Yes'),('Yes', 'No')])
    comments = TextAreaField('Comments', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Submit')


