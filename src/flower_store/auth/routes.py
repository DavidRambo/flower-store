from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from flower_store.auth.forms import LoginForm
from flower_store.models import User
from flower_store.auth import bp


@bp.route("/login", methods=["GET", "POST"])
def login():
    # In case a logged-in user navigates to the login page.
    if current_user.is_authenticated:
        return redirect(url_for("catalog.catalog"))

    form = LoginForm()
    if form.validate_on_submit():
        # Valid submitted form means POST method.
        # Try to log in with credentials in the form.
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("auth.login"))
        login_user(user)

        # Check whether user was redirected from a page that required login.
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("catalog.catalog")

        if user.is_admin:
            return redirect("admin")

        return redirect(next_page)

    # Note that the "form" referenced in the login.html template is named by the
    # keyword parmeter here, not the variable.
    return render_template("login.html", title="Log In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
