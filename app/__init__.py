__author__ = 'SWEN356 Team 4'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '\xa5\x8f\x19\xbb`$\xacw\x91\xe1\xd2\x896R\xf9\x14\x01\xe1\xd5U\xcc\xa9\x13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresl@localhost/drivertag'
db = SQLAlchemy(app)

'''from models import *'''

class Data(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     timestamp = db.Column(db.DateTime)
     x_gyroscope = db.Column(db.NUMERIC)
     y_gyroscope = db.Column(db.NUMERIC)
     z_gyroscope = db.Column(db.NUMERIC)
     x_accelorometer = db.Column(db.NUMERIC)
     y_accelorometer = db.Column(db.NUMERIC)
     z_accelorometer = db.Column(db.NUMERIC)
     latitude = db.Column(db.NUMERIC)
     longitude = db.Column(db.NUMERIC)

     ''' Foreign Key for a User '''
     user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
     user = db.relation('User', backref=db.backref('data',lazy='dynamic'))

     def __init__(self, xgyro,ygyro,zgyro,xaccel,yaccel,zaccel,latitude,longitude):
         self.x_gyroscope = xgyro
         self.y_gyroscope = ygyro
         self.z_gyroscope = zgyro
         self.x_accelorometer = xaccel
         self.y_accelorometer = yaccel
         self.z_accelorometer = zaccel
         self.latitude = latitude
         self.longitude = longitude

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))

    def __init__(self, email, name):
        self.id = email
        self.name = name


db.create_all()


from app import views
