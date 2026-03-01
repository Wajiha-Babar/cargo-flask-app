from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    plan = db.Column(db.String(20), nullable=False, default="free")  # free | premium
    role = db.Column(db.String(20), nullable=False, default="customer")  # customer | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shipments = db.relationship("Shipment", backref="owner", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_premium(self) -> bool:
        return self.plan == "premium"


class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(30), unique=True, index=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)

    weight_kg = db.Column(db.Float, nullable=False)
    distance_km = db.Column(db.Float, nullable=False, default=10)

    insurance = db.Column(db.Boolean, default=False)
    express = db.Column(db.Boolean, default=False)

    price = db.Column(db.Float, nullable=False, default=0)

    status = db.Column(db.String(50), nullable=False, default="CREATED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    events = db.relationship(
        "ShipmentEvent",
        backref="shipment",
        lazy=True,
        cascade="all, delete-orphan"
    )

class ShipmentEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey("shipment.id"), nullable=False)

    label = db.Column(db.String(80), nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)