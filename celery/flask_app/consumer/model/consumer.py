# from bson import json_util
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField,DecimalField
from wtforms.validators import InputRequired,NumberRange



class ConsumerForm(FlaskForm):
    nombre = StringField('nombre', validators=[InputRequired()])
    marca = StringField('Dias', validators=[InputRequired()])
    precio = DecimalField('precio', validators=[InputRequired(),NumberRange(min=Decimal('0.0'))])