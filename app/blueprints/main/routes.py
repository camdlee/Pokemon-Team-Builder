# ----- IMPORTS ------
from flask import render_template, request, flash
import requests
from app.blueprints.auth.forms import PokemonForm
from app.blueprints.main import main
from flask_login import login_required


# ------- ROUTES ------

#----- Home page ------
@main.route('/', methods=['GET'])
def home():
    return render_template('home.html')


#----- Pokemon API ------
@main.route('/pokemonapi', methods=['GET', 'POST'])
@login_required
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
                'Type': pokemon_data['types'][0]['type']['name'],
                'Ability': pokemon_data['abilities'][0]['ability']['name'],
                'Base_Exp': pokemon_data['base_experience'],
                'Sprite_url': pokemon_data['sprites']['front_default'],
                'Attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                'HP_base_stat': pokemon_data['stats'][0]['base_stat'],
                'Defense_base_stat': pokemon_data['stats'][2]['base_stat']
            }
            new_pokemon_data.append(pokemon_info_dict)
            return render_template('pokemonapi.html', new_pokemon_data=new_pokemon_data, form=form)
        else:
            error = 'Pokemon entry not found'
            flash(f'{error}', 'danger')
            return render_template('pokemonapi.html', form=form)
    return render_template('pokemonapi.html', form=form)


#----- Pokemon Region ------
@main.route('/pokemon_region', methods=['GET', 'POST'])
@login_required
def pokemon_region():
    return render_template('pokemon_region.html')