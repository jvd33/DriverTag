from app import db
from flask_login import UserMixin
from datetime import time

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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))

    def __init__(self, email, name):
        self.email = email
        self.name = name


class HighRiskTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    user = db.relationship('User', backref=db.backref('highrisktime', lazy='dynamic'))
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __init__(self, start_time, end_time, user_id):
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id