#-------- IMPORTS ---------
from flask import Blueprint

posts = Blueprint('posts', __name__, template_folder='posts_templates', url_prefix='/posts')

from app.blueprints.posts import routes