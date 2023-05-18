from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flower_store.admin.forms import LoginForm
from flower_store.models import Admin

admin_bp = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="templates"
)


@admin_bp.route("/admin")
@login_required
def admin():
    return render_template("admin.html", title="Admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.admin"))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is None or admin.check_password(form.password.data):
            flash("Invalid username and password.")
            return redirect(url_for("admin.login"))
        login_user(admin)
        return redirect(url_for("admin.admin"))
    return render_template("login.html", title="Log In", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))


@admin_bp.route("/add_flower")
@login_required
def add_flower():
    pass


@admin_bp.route("/update_flower/<flower_id>")
@login_required
def update_flower(flower_id):
    pass
