#---- IMPORTS -----
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# ----- INSTANCES OF PACKAGES
# Registering Packages
login = LoginManager()
# Database Manager
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # Initializing Section
    app = Flask(__name__)
    # Link to our Config
    app.config.from_object(Config)

    # Register Packages
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure Login Settings
    login.login_views = 'login'
    login.login_message = 'You must be logged in to view this page'
    login.login_message_category = 'warning'

    # Importing Blueprints
    from app.blueprints.main import main
    from app.blueprints.auth import auth

    # Registering Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
