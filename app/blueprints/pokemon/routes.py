# ----- IMPORTS ------
from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.pokemon.forms import PokemonForm
from app.blueprints.pokemon import pokemon
from flask_login import login_required, current_user
from ...models import User, Captured


# ------- ROUTES ------

#----- Pokemon API ------
@pokemon.route('/pokemonapi', methods=['GET', 'POST'])
@login_required
def pokemonapi():
    form = PokemonForm()
    print(request.method)
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
        response = requests.get(url)
        if response.ok:
            pokemon_data = response.json()
            print(pokemon_data)
            new_pokemon_data = []
            pokemon_info_dict = {
                'pokemon_name': pokemon_data["forms"][0]["name"],
                'type': pokemon_data['types'][0]['type']['name'],
                'ability': pokemon_data['abilities'][0]['ability']['name'],
                'base_exp': pokemon_data['base_experience'],
                'sprite_url': pokemon_data['sprites']['front_default'],
                'attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                'hp_base_stat': pokemon_data['stats'][0]['base_stat'],
                'defense_base_stat': pokemon_data['stats'][2]['base_stat']
            }
            for pokemon in current_user.team:
                if pokemon.pokemon_name == pokemon_info_dict['pokemon_name']:
                    flash(f'That pokemon is already on your team! Please choose another.', 'danger')
                    return redirect(url_for('pokemon.pokemonapi'))
            new_pokemon_data.append(pokemon_info_dict)
            return render_template('pokemonapi.html', new_pokemon_data=new_pokemon_data, form=form)
        else:
            error = 'Pokemon entry not found'
            flash(f'{error}', 'danger')
            return render_template('pokemonapi.html', form=form)
    return render_template('pokemonapi.html', form=form)

# ---- View pokemon team -----
@pokemon.route('/pokemon_team')
@login_required
def pokemon_team():
    my_team = current_user.team
    return render_template('pokemon_team.html', my_team=my_team)


# ----- Catch Pokemon ------
@pokemon.route('/catch/<pokemon_name>')
@login_required
def catch(pokemon_name):
    # will query table to see if pokemon is in caught table
    captured_pokemon = Captured.query.filter_by(pokemon_name=pokemon_name).first()
    form = PokemonForm()
    
    if captured_pokemon:
        if current_user.team.count() < 5:
            current_user.catch(captured_pokemon)
            flash(f'Successfully caught {pokemon_name}!', 'success')
            return redirect (url_for('pokemon.pokemonapi'))
        else:
            flash(f'Warning Team is full!', 'warning')
            return redirect (url_for('pokemon.pokemonapi'))
    else:
        if current_user.team.count() < 5:
            pokemon_name = pokemon_name
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
            response = requests.get(url)
            if response.ok:
                pokemon_data = response.json()
                print(pokemon_data)
                pokemon_info_dict = {
                    'pokemon_name': pokemon_data["forms"][0]["name"].title(),
                    'type': pokemon_data['types'][0]['type']['name'],
                    'ability': pokemon_data['abilities'][0]['ability']['name'],
                    'base_exp': pokemon_data['base_experience'],
                    'sprite_url': pokemon_data['sprites']['front_default'],
                    'attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                    'hp_base_stat': pokemon_data['stats'][0]['base_stat'],
                    'defense_base_stat': pokemon_data['stats'][2]['base_stat']
                }
                new_pokemon = Captured()
                new_pokemon.from_dict(pokemon_info_dict)
                new_pokemon.save_to_db()

                current_user.catch(new_pokemon)            
                return redirect (url_for('pokemon.pokemonapi'))
    return redirect (url_for('pokemon.pokemonapi'))



# ------ Remove a Pokemon from Team ------
@pokemon.route('/remove/<pokemon_name>')
@login_required
def remove(pokemon_name):
    my_team = current_user.team
    for pokemon in my_team:
        if pokemon.pokemon_name == pokemon_name:
            current_user.remove(pokemon)
            flash(f'Successfully removed {pokemon.pokemon_name} from team!', 'success')
    return redirect (url_for('pokemon.pokemon_team'))



# #----- Pokemon Region ------
# @pokemon.route('/pokemon_region', methods=['GET', 'POST'])
# @login_required
# def pokemon_region():
#     return render_template('pokemon_region.html')

# if current_user.captured_pokemon.count() >= 5:
#         flash('You already have 5 pokemon on your team!', 'danger')
#         return redirect(url_for('main.pokemon_form'))