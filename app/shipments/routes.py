import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Shipment, ShipmentEvent
from ..utils import calc_price
from .forms import ShipmentCreateForm

bp = Blueprint("shipments", __name__)

def generate_tracking():
    return "TRK-" + secrets.token_hex(4).upper()

@bp.route("/")
@login_required
def list_shipments():
    shipments = (
        Shipment.query
        .filter_by(user_id=current_user.id)
        .order_by(Shipment.created_at.desc())
        .all()
    )
    return render_template("shipments/list.html", shipments=shipments)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ShipmentCreateForm()
    if form.validate_on_submit():
        insurance = bool(form.insurance.data)
        express = bool(form.express.data)

        if (insurance or express) and not current_user.is_premium:
            flash("Insurance/Express are Premium features. Upgrade your plan from Profile.", "warning")
            return render_template("shipments/create.html", form=form)

        price = calc_price(
            weight_kg=form.weight_kg.data,
            distance_km=form.distance_km.data,
            express=express,
            insurance=insurance,
        )

        shipment = Shipment(
            tracking_number=generate_tracking(),
            user_id=current_user.id,
            origin=form.origin.data,
            destination=form.destination.data,
            weight_kg=form.weight_kg.data,
            distance_km=form.distance_km.data,
            insurance=insurance,
            express=express,
            price=price,
            status="CREATED",
        )
        db.session.add(shipment)
        db.session.flush()

        db.session.add(ShipmentEvent(
            shipment_id=shipment.id,
            label="CREATED",
            note="Shipment created",
        ))
        db.session.commit()

        flash("Shipment created successfully.", "success")
        return redirect(url_for("shipments.detail", shipment_id=shipment.id))

    return render_template("shipments/create.html", form=form)

@bp.route("/<int:shipment_id>")
@login_required
def detail(shipment_id: int):
    shipment = db.session.get(Shipment, shipment_id)
    if not shipment or shipment.user_id != current_user.id:
        abort(404)

    shipment.events.sort(key=lambda e: e.created_at, reverse=True)
    return render_template("shipments/detail.html", shipment=shipment)