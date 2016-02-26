from app import db

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

     def __int__(self, xgyro,ygyro,zgyro,xaccel,yaccel,zaccel,latitude,longitude):
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
