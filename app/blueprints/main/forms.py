# -------- IMPORTS ---------
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField,StringField
from wtforms.validators import DataRequired, EqualTo
from app.models import User

# ------ Pokedex Form ------
class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')