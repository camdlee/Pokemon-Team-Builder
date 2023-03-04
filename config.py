
# ----- IMPORTS ------
import os

#------ CONFIG -----
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    POKEMON_REGIONS = {
        '1': 'Kanto',
        '2': 'Jhoto',
        '3': 'Hoenn',
        '4': 'Sinnoh',
        '5': 'Unova',
    }