from flask import Blueprint
from flask import render_template

error = Blueprint('error', __name__)

@error.app_errorhandler(403)
def forbidden(e):
    return render_template('error.html', error_code=403, error_msg="Accesso negato!"), 403

@error.app_errorhandler(404)
def page_not_found(e):
     return render_template('error.html', error_code=404, error_msg="File non trovato!"), 404

@error.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_msg="Errore interno al server!"), 500
