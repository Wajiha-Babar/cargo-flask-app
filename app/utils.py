from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapped

def calc_price(weight_kg: float, distance_km: float, express: bool, insurance: bool) -> float:
    """
    Simple pricing engine (mock):
    base = 250
    per_kg = 35
    per_km = 2.5
    express multiplier = 1.35
    insurance adds 120
    """
    base = 250
    price = base + (35 * float(weight_kg)) + (2.5 * float(distance_km))
    if express:
        price *= 1.35
    if insurance:
        price += 120
    return round(price, 2)