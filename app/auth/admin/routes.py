from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from ..extensions import db
from ..models import Shipment, ShipmentEvent
from ..utils import admin_required
from .forms import ShipmentStatusForm

bp = Blueprint("admin", __name__)

@bp.route("/shipments")
@login_required
@admin_required
def shipments():
    shipments = Shipment.query.order_by(Shipment.created_at.desc()).all()
    return render_template("admin/shipments.html", shipments=shipments)

@bp.route("/shipments/<int:shipment_id>", methods=["GET", "POST"])
@login_required
@admin_required
def shipment_detail(shipment_id: int):
    shipment = db.session.get(Shipment, shipment_id)
    if not shipment:
        return render_template("admin/shipment_detail.html", shipment=None, form=None), 404

    form = ShipmentStatusForm(status=shipment.status)
    if form.validate_on_submit():
        shipment.status = form.status.data
        db.session.add(ShipmentEvent(
            shipment_id=shipment.id,
            label=form.status.data,
            note=form.note.data or "Status updated by admin",
        ))
        db.session.commit()
        flash("Status updated.", "success")
        return redirect(url_for("admin.shipment_detail", shipment_id=shipment.id))

    shipment.events.sort(key=lambda e: e.created_at, reverse=True)
    return render_template("admin/shipment_detail.html", shipment=shipment, form=form)