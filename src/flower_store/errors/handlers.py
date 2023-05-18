from flask import Blueprint, render_template

bp = Blueprint("errors", __name__)


@bp.app_errorhandler(404)
def error_404(error):
    """An error handler that works much like a route, returns a template url
    and the int representing the error code.
    """
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html"), 403


@bp.app_errorhandler(AttributeError)
def error_406(error):
    return render_template("errors/406.html"), 406


@bp.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html"), 500
