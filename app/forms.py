
# ----- Imports ------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# ------ Pokemon Form ------
class PokemonForm(FlaskForm):
    pokemon_name = StringField('pokemon_name', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')
