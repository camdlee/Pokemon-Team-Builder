# ----- IMPORTS ------
from flask import render_template
from app import app
from models import User


# ------- ROUTES ------

#----- Home page ------
@app.route('/', methods=['GET'])
def home():
    users = User.query.all()
    return render_template('home.html', users=users)