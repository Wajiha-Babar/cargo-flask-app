from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Shipment

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def dashboard():
    shipments = Shipment.query.filter_by(user_id=current_user.id).order_by(Shipment.created_at.desc()).limit(5).all()
    total = Shipment.query.filter_by(user_id=current_user.id).count()
    return render_template("main/dashboard.html", shipments=shipments, total=total)

@bp.route("/pricing")
def pricing():
    return render_template("main/pricing.html")

@bp.route("/profile")
@login_required
def profile():
    return render_template("main/profile.html")

@bp.route("/upgrade", methods=["POST"])
@login_required
def upgrade():
    # Mock upgrade (later Stripe)
    current_user.plan = "premium"
    db.session.commit()
    flash("Upgraded to Premium (mock). Now you can use Insurance/Express.", "success")
    return redirect(url_for("main.profile"))