from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import *
from decimal import Decimal
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresl@localhost/drivertag'
db = SQLAlchemy(app)

''' Clean out data '''
db.engine.execute('delete from data')
db.engine.execute('delete from \"user\"')


'''Create fake users'''
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



'''
    This function shall find a new datapoint that satisfies the following requirements

    1) generates a change in x Delta
    2) Randomly either decreases or increases the data point

'''
def generateNormalDataPoint(previousX,previousY,previousZ, currentUser):

    '''Generate random acceleration changes for x,y,z '''
    xDelta = previousX + Decimal(random.uniform(-.12,.12))
    yDelta = previousY + Decimal(random.uniform(-.05,.05))
    zDelta = previousZ + Decimal(random.uniform(-.09,.09))

    dataPoint = Data( xDelta, yDelta, zDelta, currentUser)
    return dataPoint

'''
    This Function generates a datapoint for the start of a Accel event
'''

def startAccelEvent(currentUser,swerve):


    ''' Generate Either Negative (braking) or Positive X datapoint '''
    if(random.randint(0,1) == 0):
        xDelta = 0 - Decimal(random.uniform(.90,1.65))
    else:
        xDelta = random.uniform(.90,1.65)

    ''' Generate Either Negative (braking) or Positive Z datapoint '''
    if(random.randint(0,1) == 0) & (swerve == True):
         zDelta = 0 - Decimal(random.uniform(.25,.70))
    elif swerve == True:
        zDelta = random.uniform(.25,.70)
    else:
        zDelta = random.uniform(-.13,.13)


    yDelta =  random.uniform(-.05,.05)

    dataPoint = Data( xDelta, yDelta, zDelta, currentUser)

    return dataPoint

def continueAccelEvent(previousX,previousY,previousZ, currentUser):

    '''Generate random acceleration changes for x,y,z '''
    xDelta = Decimal(previousX) + Decimal(random.uniform(-.12,.12))
    yDelta = Decimal(previousY) + Decimal(random.uniform(-.05,.05))
    zDelta = Decimal(previousZ) + Decimal(random.uniform(-.09,.09))

    dataPoint = Data( xDelta, yDelta, zDelta, currentUser)

    return dataPoint

''' Generate a datapoint for the end of an acceleration '''
def endAccelEvent(currentUser):

    '''Generate random acceleration changes for x,y,z '''
    xDelta = random.uniform(-.10,.10)
    yDelta = random.uniform(-.05,.05)
    zDelta = random.uniform(-.09,.09)

    dataPoint = Data( xDelta, yDelta, zDelta, currentUser)
    return dataPoint


'''Constants for sensor data '''

'''Polling Rate in seconds'''
SensorInterval = 1


''' For each user generate data'''
for currentUser in userArray:

    print('Seeding data for user is', currentUser.name)
    random.seed(currentUser.name)

    '''create random maxVariance per user '''
    ''' maxVariance = random variance '''

    '''2-8 hours of simulated data for a given user '''
    hours = random.uniform(2,8)

    ''' Number of time steps to simulate '''
    numSteps = round((hours *60 *60)/SensorInterval)

    print("Number of steps: ", numSteps)

    '''
        Need to generate the first Data point for the user

        example: The application has started recording data
        because the user is about to start their trip
    '''

    dataPoint = Data(0, 0, 0, currentUser)
    db.session.add(dataPoint)
    db.session.commit()

    timeLeftAccel = 0
    critical = False
    swerve = False

    dataList = []

    ''' Generate each timeStep '''
    for num in range(numSteps-1):
        ''' Generate new data points for a user '''


        chanceToLive = round(random.random(),4)

        ''' Continued Accel Event '''
        if (critical==True):
            ''' Reduce the time left for the Acceleration '''
            timeLeftAccel = timeLeftAccel -1
            ''' Generate DataPoint '''
            dataPoint = continueAccelEvent(dataPoint.x_accelorometer,dataPoint.y_accelorometer,dataPoint.z_accelorometer,currentUser)

        # Start Accel Event
        elif (chanceToLive < .013) :

            #Accel Event Flag
            critical = True

            ''' The car swerved (Implication on Z acceleration)'''
            if(random.randint(0,1)==0):
                swerve = True

            ''' The length of the acceleration 1-4 seconds'''
            timeLeftAccel = random.randint(1,4)

            ''' Generate DataPoint '''
            dataPoint =startAccelEvent(currentUser,swerve)


        # End of Accel Event
        elif timeLeftAccel < 0 :
            timeLeftAccel = 0
            critical = False
            swerve = False
            dataPoint = endAccelEvent(currentUser)

        # Normal Driving
        else:
            dataPoint = generateNormalDataPoint(dataPoint.x_accelorometer,dataPoint.y_accelorometer,dataPoint.z_accelorometer,currentUser)




        ''' We may add the array instead of each individual dataPoint '''
        dataList.append(dataPoint)

    ''' Bulk Insert '''
    db.session.add_all(dataList)
    db.session.commit()


