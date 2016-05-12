__author__ = 'SWEN356 Team 4'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = '\xa5\x8f\x19\xbb`$\xacw\x91\xe1\xd2\x896R\xf9\x14\x01\xe1\xd5U\xcc\xa9\x13'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from app import models

db.create_all()

from app import views

