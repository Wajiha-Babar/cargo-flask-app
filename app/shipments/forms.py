from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ShipmentCreateForm(FlaskForm):
    origin = StringField("Origin", validators=[DataRequired(), Length(max=120)])
    destination = StringField("Destination", validators=[DataRequired(), Length(max=120)])

    weight_kg = FloatField("Weight (kg)", validators=[DataRequired(), NumberRange(min=0.1)])
    distance_km = FloatField("Distance (km)", validators=[DataRequired(), NumberRange(min=1)])

    insurance = BooleanField("Insurance (Premium)")
    express = BooleanField("Express Delivery (Premium)")

    submit = SubmitField("Create Shipment")