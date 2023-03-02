
# ----- Imports ------
from flask import Flask
from config import Config

#----- Initializing Section ------
app = Flask(__name__)
app.config.from_object(Config)

from app import routes