#-------- IMPORTS ---------
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='auth/')

from app.blueprints.auth import routes