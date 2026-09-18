from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Anyone without a profile yet (including accounts created before
    # this feature existed) gets sent to fill it in first.
    if current_user.profile is None:
        return redirect(url_for("profile.setup"))
    return render_template("dashboard.html", user=current_user)
