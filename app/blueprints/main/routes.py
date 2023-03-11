# ----- IMPORTS ------
from flask import render_template, request, flash
import requests
from app.blueprints.main import main
from flask_login import login_required
from ...models import User


# ------- ROUTES ------

#----- Home page ------
@main.route('/', methods=['GET'])
def home():
    users = User.query.all()
    return render_template('home.html', users=users)
