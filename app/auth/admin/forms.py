from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ShipmentStatusForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[
            ("CREATED", "CREATED"),
            ("PICKED_UP", "PICKED_UP"),
            ("IN_TRANSIT", "IN_TRANSIT"),
            ("OUT_FOR_DELIVERY", "OUT_FOR_DELIVERY"),
            ("DELIVERED", "DELIVERED"),
            ("CANCELLED", "CANCELLED"),
        ],
        validators=[DataRequired()]
    )
    note = StringField("Event note", validators=[Length(max=255)])
    submit = SubmitField("Update Status")