from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bkgffbntgqbhdo:c2f4a4ad80eb32b3fe9363aaebf01604d9988f6c141b621e7ccf2a21b65535c9@ec2-54-146-91-153.compute-1.amazonaws.com:5432/dand601ul88o87'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

from project.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


# Blueprints
from project.users import users_bp

app.register_blueprint(users_bp)


# General views
from . import views

db.create_all()
