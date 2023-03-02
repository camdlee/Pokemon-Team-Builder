
# ----- Imports ------
from flask import render_template, request
from app import app
import requests
from app.forms import PokemonForm

#----- Home page ------
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', methods=['GET'])


#----- Pokemon API ------
@app.route('/pokemonapi', methods=['GET', 'POST'])
def pokemonapi():
    form = PokemonForm()
    print(request.method)
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
        response = requests.get(url)
        if response.ok:
            pokemon_data = response.json()
            print(pokemon_data)
            new_pokemon_data = []
            pokemon_info_dict = {
                'Name': pokemon_name.title(),
                'Ability': pokemon_data['abilities'][0]['ability']['name'],
                'Base_Exp': pokemon_data['base_experience'],
                'Sprite_url': pokemon_data['sprites']['front_shiny'],
                'Attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                'HP_base_stat': pokemon_data['stats'][0]['base_stat'],
                'Defense_base_stat': pokemon_data['stats'][2]['base_stat']
            }
            new_pokemon_data.append(pokemon_info_dict)
            return render_template('pokemonapi.html', new_pokemon_data=new_pokemon_data, form=form)
        else:
            error = 'Pokemon does not exist. Please type in a pokemon'
            return render_template('pokemonapi.html', form=form, error=error)
    return render_template('pokemonapi.html', form=form)