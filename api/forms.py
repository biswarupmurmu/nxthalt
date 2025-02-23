# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class TravelForm(FlaskForm):
    source = StringField('Source', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    hour = IntegerField('Time (in hours)', default=0, validators=[NumberRange(min=0, max=23)])
    minutes = IntegerField('Time (in minutes)', default=0, validators=[NumberRange(min=0, max=59)])
    submit = SubmitField('Find')

