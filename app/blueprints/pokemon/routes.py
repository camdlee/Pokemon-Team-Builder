# ----- IMPORTS ------
from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.pokemon.forms import PokemonForm
from app.blueprints.pokemon import pokemon
from flask_login import login_required, current_user
from ...models import User, Captured


# ------- ROUTES ------

#----- Pokemon API Search ------
@pokemon.route('/pokemonapi', methods=['GET', 'POST'])
@login_required
def pokemonapi():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
        response = requests.get(url)
        if response.ok:
            pokemon_data = response.json()
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
@pokemon.route('/catch/<pokemon_name>', methods=['GET', 'POST'])
@login_required
def catch(pokemon_name):
    # will query table to see if pokemon is in caught table
    captured_pokemon = Captured.query.filter_by(pokemon_name=pokemon_name).first()
    form = PokemonForm()
    print(captured_pokemon)

    if captured_pokemon:
        if current_user.team.count() < 5:
            print('check count')
            current_user.catch(captured_pokemon)
            flash(f'Successfully caught {pokemon_name}!', 'success')
            return redirect (url_for('pokemon.pokemonapi'))
        else:
            flash('Warning Team is full!', 'warning')
            return redirect (url_for('pokemon.pokemonapi'))
    else:
        if current_user.team.count() < 5:
            pokemon_name = pokemon_name
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
            response = requests.get(url)
            if response.ok:
                pokemon_data = response.json()
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
                for pokemon in current_user.team:
                    if pokemon.pokemon_name == pokemon_info_dict['pokemon_name']:
                        flash(f'That pokemon is already on your team! Please choose another pokemon.', 'danger')
                        return redirect(url_for('pokemon.pokemonapi'))
                new_pokemon = Captured()
                new_pokemon.from_dict(pokemon_info_dict)
                new_pokemon.save_to_db()

                current_user.catch(new_pokemon)
                flash(f'Successfully caught {pokemon_name}!', 'success')            
                return redirect (url_for('pokemon.pokemonapi'))
        else:
            flash('Warning Team is full!', 'warning')
            return redirect (url_for('pokemon.pokemonapi'))
    return redirect (url_for('pokemon.pokemonapi'))



# ------ Remove a Pokemon from Team ------
@pokemon.route('/remove/<pokemon_name>', methods=['GET', 'POST'])
@login_required
def remove(pokemon_name):
    my_team = current_user.team
    for pokemon in my_team:
        if pokemon.pokemon_name == pokemon_name:
            current_user.remove(pokemon)
            flash(f'Successfully removed {pokemon.pokemon_name} from team!', 'success')
    return redirect (url_for('pokemon.pokemon_team'))


# --------- Battle Arena ---------
@pokemon.route('/battle_arena')
@login_required
def battle_arena():
    users = User.query.all()
    return render_template('battle_arena.html', users=users)


# --------- Battle Opponent ---------
@pokemon.route('/battle/<int:id>', methods=['GET', 'POST'])
@login_required
def battle(id):
    opponent = User.query.get(id)

    user_final_stats = current_user.max_defense()+current_user.max_hp() - opponent.max_attack()
    opponent_final_stats = opponent.max_defense()+opponent.max_hp() - current_user.max_attack()

    if user_final_stats > opponent_final_stats:
        flash(f"You won! Your team was stronger than {opponent.first_name}'s team", 'success')
        return redirect(url_for('pokemon.battle_arena'))
    elif user_final_stats == opponent_final_stats:
        flash(f"It's a tie! Both of your teams are equally matched", 'warning')
        return redirect(url_for('pokemon.battle_arena'))
    else:
        flash(f"Sorry you lost to {opponent.first_name}!", 'danger')
        return redirect(url_for('pokemon.battle_arena'))
    

# # --------- View Opponent's Team ---------
# @pokemon.route('/<opponent>_team', methods=['GET', 'POST'])
# @login_required
# def opponent_team(id):
#     opponent = User.query.get(id)

