from flask_sqlalchemy import SQLAlchemy
from flaskcarapp import app
from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import UserMixin
from flaskcarapp import login_manager

db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)
    post = db.relationship('Post',backref="author",lazy=True)
    
    
    def __init__(self,username, email, password):
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def __repr__(self):
        return "{} has been created".format(self.username)

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

class LoginForm(db.Model):
    email = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.email
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(290))
    data_created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return "The title is {} and the user is {}".format(self.title,self.user_id)
