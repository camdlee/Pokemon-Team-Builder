# -------- IMPORTS ---------
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField
from wtforms.validators import DataRequired

# ------ Pokedex Form ------
class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')
    catch_btn = SubmitField('Catch')

# # ------ Catch Pokemon Form ------
# class CatchPokemonForm(FlaskForm):
#     submit_btn = SubmitField('Submit')

# # ------ Pokemon Team From -------
# class PokemonTeamForm(FlaskForm):
#     team = StringField('')