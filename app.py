from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

class PokemonForm(FlaskForm):
    pokemon_name = StringField('name', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', methods=['GET'])

@app.route('/pokemonapi', methods=['GET', 'POST'])
def pokemonapi():
    form = PokemonForm()
    print(request.method)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.pokemon_name.data
        print(name)
        url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
        response = requests.get(url)
        if response.ok:
            pokemon_data = response.json()
            print(pokemon_data)
            new_pokemon_data = []
            pokemon_info_dict = {
                'Name': name.title(),
                'Ability': pokemon_data['abilities'][0]['ability']['name'],
                'Base_Exp': pokemon_data['base_experience'],
                'Sprite_url': pokemon_data['sprites']['front_shiny'],
                'Attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                'HP_base_stat': pokemon_data['stats'][0]['base_stat'],
                'Defense_base_stat': pokemon_data['stats'][2]['base_stat']
            }
            new_pokemon_data.append(pokemon_info_dict)
            return render_template('pokemonapi.html', new_pokemon_data=new_pokemon_data)
        else:
            return 'Pokemon does not exist.'
    return render_template('pokemonapi.html')