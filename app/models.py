from app import db
from flask_login import UserMixin
from datetime import datetime

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
     '''user = db.relation('User', backref=db.backref('data',lazy='dynamic'))'''

     def __init__(self, xaccel,yaccel,zaccel, time, user):
         self.x_accelorometer = xaccel
         self.y_accelorometer = yaccel
         self.z_accelorometer = zaccel
         self.timestamp = time
         self.user_id = user.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    data = db.relationship('Data', backref='user',lazy='dynamic')
    accel = db.relationship('Acceleration', backref='accel', uselist=False)
    addr = db.relationship('Address', backref='addr', uselist=False)

    def __init__(self, email, name):
        self.email = email
        self.name = name
        self.accel = Acceleration(20, 1, self.id)


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


class Acceleration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), unique=True)
    delta_mph = db.Column(db.DECIMAL)
    seconds = db.Column(db.DECIMAL)
    g = db.Column(db.DECIMAL)

    def __init__(self, mph, s, user_id):
        self.mph = mph
        self.seconds = s
        self.user_id = user_id
        self.g = float((mph/s)) * .045585  # in gs!


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), unique=True)
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(5))
    radius = db.Column(db.INTEGER)

    def __init__(self, a, c, s, z, r, id):
        self.street = a
        self.city = c
        self.state = s
        self.zip = z
        self.radius = r
        self.user_id = id

    def __str__(self):
        return "%s %s %s %s with a danger radius of %d miles" \
               % (self.street, self.city, self.state, self.zip, self.radius)
