__author__ = 'SWEN356 Team 4'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '\xa5\x8f\x19\xbb`$\xacw\x91\xe1\xd2\x896R\xf9\x14\x01\xe1\xd5U\xcc\xa9\x13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresl@localhost/drivertag'
db = SQLAlchemy(app)
db.drop_all()  # THIS IS FOR DEVELOPMENT!
login_manager = LoginManager()
login_manager.init_app(app)

from app import models

db.create_all()

from app import views
