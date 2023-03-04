
# ----- IIMPORTS ------
from flask import render_template, request, flash, redirect, url_for
import requests
from app.forms import PokemonForm, RegistrationForm, LoginForm
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user



# ------- ROUTES ------

#----- Home page ------
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# ------ Registration Page ------
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        # Grabbing our form data and storing into a dict
        new_user_data ={
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.email.data
        }

        # Create instance of User
        new_user = User()
        
        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save to our database
        new_user.save_to_db()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# ------ Login Page ------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        
        # Query from database
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully Logged In! Welcome back, {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password'
            flash(f'{error}', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


# ------ Logout Page ------
@app.route('/logout', methods=['GET'])
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'warning')
        return redirect(url_for('login')) 
    

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

    