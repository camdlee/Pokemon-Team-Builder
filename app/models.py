
# -------- IMPORTS ---------
from app import db, login
from flask_login import UserMixin # Only use on your User Class
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

pokemon_team = db.Table('pokemon_team', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('captured.id'))    
)


# -------- CLASSES ---------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    team = db.relationship('Captured',
                secondary = pokemon_team,
                backref = 'owner',
                lazy = 'dynamic')
    
    # hashes our password
    def hash_password(self, original_password): 
        return generate_password_hash(original_password)
    
    # check password hash
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password) 
    
    # Use this method to register our user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def update_from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']

    # Save to our database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # catch to team
    def catch(self, pokemon):
        self.team.append(pokemon)
        db.session.commit()

    # remove from team
    def remove(self, pokemon):
        self.team.remove(pokemon)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Captured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String)
    pokemon_type = db.Column(db.String)
    ability = db.Column(db.String)
    base_exp = db.Column(db.String)
    sprite_url = db.Column(db.String)
    attack_base_stat = db.Column(db.String)
    hp_base_stat = db.Column(db.String)
    defense_base_stat = db.Column(db.String)

    # Use this method to register our pokemon attributes
    def from_dict(self, data):
        self.pokemon_name = data['name']
        self.pokemon_type = data['type']
        self.ability = data['ability']
        self.base_exp = data['base_exp']       
        self.sprite_url = data['sprite_url']
        self.attack_base_stat = data['attack_base_stat']
        self.hp_base_stat = data['hp_base_stat']
        self.defense_base_stat = data['defense_base_stat']

    # Save the pokemon to the captured database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Update database
    def update_db(self):
        db.session.commit()        

    # Release the pokemon from the captured database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
