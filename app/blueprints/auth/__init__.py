#-------- IMPORTS ---------
from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='auth_templates')

from app.blueprints.auth import routes