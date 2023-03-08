#-------- IMPORTS ---------
from flask import Blueprint

pokemon = Blueprint('pokemon', __name__, template_folder='pokemon_templates')

from app.blueprints.pokemon import routes