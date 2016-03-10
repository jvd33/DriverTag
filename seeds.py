from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresl@localhost/drivertag'
db = SQLAlchemy(app)

from app.models import User
user1 = User('1@test.com', 'Tim Smith')
user2 = User('2@test.com', 'Matt Smith')
user3 = User('3@test.com', 'Bob Smith')
user4 = User('4@test.com', 'Johnny Smith')
user5 = User('5@test.com', 'Rob Smith')
user6 = User('6@test.com', 'Xavier Smith')
user7 = User('7@test.com', 'Brandon Smith')
user8 = User('8@test.com', 'Paul Smith')
user9 = User('9@test.com', 'Brady Smith')
userArray = [user1, user2, user3, user4, user5, user6, user7, user8, user9]
db.session.add_all(userArray)
db.session.commit()


from app.models import Data

'''Constans for sensor data '''

'''Polling Rater in ms'''
SensorInterval = 100

'''number of hours to simulate data for users '''
hours = 5

''' Number of time steps to simulate '''
numSteps = (hours *60 *60 *1000)/SensorInterval

''' For each user generate data'''
for currentUser in userArray:
    '''create random variance per user '''
    ''' variance = random variance '''


    ''' Generate each timeStep '''
    for num in range(numSteps):
        ''' Generate new data points for a user '''

        '''
        These numbers need to be random but realistic
        1) needs to be continuous
        2) needs to be a normal distribution

        code that may be useful
        round(random.uniform(-3,3),4)

        x = random number
        y = random number
        z = random number

        dataPoint = Data(x, y, z, currentUser)

        db.session.add(dataPoint)
        db.session.commit()

        '''

