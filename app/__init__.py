from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import os
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Just Try To Guess'
app.config['POSTS_PER_PAGE'] = 3
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
moment = Moment(app)

migrate = Migrate(app,db)

from app import views, models

