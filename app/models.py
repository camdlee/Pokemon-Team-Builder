
# -------- IMPORTS ---------
from app import db, login
from flask_login import UserMixin # Only use on your User Class
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

followers = db.Table(
    'follower', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)

# Could do it this way but above is preferred
# class Followers(db.Model):
#     follower_id = db.Column('follower_id', db.Integer, db.ForeignKey('user.id'))
#     followed_id = db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),


# -------- CLASSES ---------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
        secondary = followers,
        primaryjoin = (followers.columns.follower_id == id), 
        secondaryjoin = (followers.columns.followed_id == id),
        backref = db.backref('followers', lazy='dynamic'),
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
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    caption = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key to User Table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # another way to do it is :
    #user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    # Use this method to register our user attributes
    def from_dict(self, data):
        self.img_url = data['img_url']
        self.title = data['title']
        self.caption = data['caption']
        self.user_id = data['user_id']

    # Save to our database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

# class CatchPokemon(db.Model):
    