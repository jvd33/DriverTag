from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table
from app.models import *
from decimal import Decimal
from datetime import *
import logging
import random
import os
from pykml import parser



'''Constants for sensor data '''

'''Polling Rate in seconds'''
SENSORINTERVAL = 1
''' Minumum amount of hours '''
MINUMUMHOURS = 2
''' Maximum amount of hours '''
MAXIMUMHOURS = 8
''' Number of days to generate data for'''
NUMOFDAYS = 1
''' Min Number of minutes a high risk time can last '''
MINHIGHRISKMINUTES = 10
''' Max Number of minutes a high risk time can last '''
MAXHIGHRISKMINUTES = 60


"""
Parse a well formatted path for map display, assign to a specific user (3)
"""

def parse_map_user(user):

    kml = os.path.join(os.getcwd(), 'data.kml')
    with open(kml) as f:
        doc = parser.fromstring(f.read())
        coords = doc.Document.Folder.Placemark.LineString.coordinates[0].text.strip().split()
        points = [(x.split(',')[0], x.split(',')[1]) for x in coords]

    for p in points:
        d = Data(0, 0, 0, p[1], p[0], datetime.now(), user)
        db.session.add(d)


    db.session.commit()

'''
    This function shall find a new datapoint that satisfies the following requirements

    1) generates a change in x Delta
    2) Randomly either decreases or increases the data point

'''
def GenerateNormalDataPoint(time, currentUser, latitude, longitude):

    '''Generate random acceleration changes for x,y,z '''
    xDelta = Decimal(random.uniform(-.22,.22))
    yDelta = Decimal(random.uniform(-.07,.07))
    zDelta = Decimal(random.uniform(-.11,.11))

    #generate new gps coordinates
    latitude,longitude = GenerateGPSPoint(latitude, longitude)

    dataPoint = Data( xDelta, yDelta, zDelta, latitude, longitude, time, currentUser)
    return dataPoint

'''
    This Function generates a datapoint for the start of a Accel event
'''

def StartAccelEvent(time, currentUser, swerve, latitude, longitude):


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

    #generate new gps coordinates
    latitude,longitude = GenerateGPSPoint(latitude, longitude)

    dataPoint = Data( xDelta, yDelta, zDelta, latitude, longitude, time, currentUser)

    return dataPoint

def ContinueAccelEvent(time, previousX, previousY, previousZ, currentUser, latitude, longitude):

    '''Generate random acceleration changes for x,y,z '''
    xDelta = Decimal(previousX) + Decimal(random.uniform(-.12,.12))
    yDelta = Decimal(previousY) + Decimal(random.uniform(-.05,.05))
    zDelta = Decimal(previousZ) + Decimal(random.uniform(-.09,.09))

    #generate new gps coordinates
    latitude,longitude = GenerateGPSPoint(latitude, longitude)

    dataPoint = Data( xDelta, yDelta, zDelta, latitude, longitude, time,  currentUser)

    return dataPoint

'''
    This function Generate a datapoint for the end of an acceleration
'''
def EndAccelEvent(time, currentUser, latitude, longitude):

    '''Generate random acceleration changes for x,y,z '''
    xDelta = random.uniform(-.10,.10)
    yDelta = random.uniform(-.05,.05)
    zDelta = random.uniform(-.09,.09)

    #generate new gps coordinates
    latitude,longitude = GenerateGPSPoint(latitude, longitude)

    dataPoint = Data( xDelta, yDelta, zDelta, latitude, longitude, time, currentUser)
    return dataPoint

'''
    This function modifies existing latitude and longitudes positions randomly to simulate that the user is moving
'''
def GenerateGPSPoint(latitude, longitude):

    latitude = round((Decimal(latitude) + Decimal(random.uniform(-.05, .05))), 6)
    longitude = round((Decimal(longitude) + Decimal(random.uniform(-.05, .05))), 6)

    return latitude, longitude

def GenerateHighRiskTime(timeStamp, currentUser):
    EndHighRiskTime = timeStamp + timedelta(minutes=random.randint(MINHIGHRISKMINUTES,MAXHIGHRISKMINUTES))

    newHighRiskTime = HighRiskTime(timeStamp,EndHighRiskTime, currentUser.id)

    db.session.add(newHighRiskTime)
    #db.session.commit()

    return

'''
    This function generates data for a user of the course of the entire day
'''
def GenerateDay(timeStamp):

    ''' For each user generate data'''
    for currentUser in userArray:

        print('Seeding data for user', currentUser.name)
        random.seed(currentUser.name)



        '''2-8 hours of simulated data for a given user '''
        hours = random.uniform(MINUMUMHOURS,MAXIMUMHOURS)

        ''' Number of time steps to simulate '''
        numSteps = round((hours *60 *60) / SENSORINTERVAL)

        logging.debug("Number of steps: ", numSteps)

        '''
            Need to generate the first Data point for the user

            example: The application has started recording data
            because the user is about to start their trip
        '''

        latitude = 43.084389
        longitude = -77.673769

        dataPoint = Data(0, 0, 0, latitude, longitude, timeStamp, currentUser)
        db.session.add(dataPoint)
        db.session.commit()

        timeLeftAccel = 0
        critical = False
        swerve = False

        dataList = []

        ''' Generate each timeStep '''
        for num in range(numSteps-1):
            ''' Generate new data points for a user '''

         #add time interval to the timestamp
            timeStamp = timeStamp + timedelta(0, SENSORINTERVAL)

            ChanceForHighRiskTimeCreation = random.random()

            #Create a highRisk time starting at this point in time
            if (ChanceForHighRiskTimeCreation < .0001) :
                GenerateHighRiskTime(timeStamp, currentUser)

            '''
                This section generates acceleration and gps data
            '''

            ChanceForAccelerationEvent = round(random.random(),4)


            ''' Continued Accel Event '''
            if critical is(True) and timeLeftAccel > 0:
                ''' Reduce the time left for the Acceleration '''
                timeLeftAccel-=1
                ''' Generate DataPoint '''
                dataPoint = ContinueAccelEvent(timeStamp, dataPoint.x_accelorometer, dataPoint.y_accelorometer, dataPoint.z_accelorometer, currentUser, latitude, longitude)

            # Start Accel Event
            elif (ChanceForAccelerationEvent < .013) :

                #Accel Event Flag
                critical = True

                ''' The car swerved (Implication on Z acceleration)'''
                if(random.randint(0,1)==0):
                    swerve = True

                ''' The length of the acceleration 1-4 seconds'''
                timeLeftAccel = random.randint(1,4)

                ''' Generate DataPoint '''
                dataPoint = StartAccelEvent(timeStamp, currentUser, swerve, latitude, longitude)

            # End of Accel Event
            elif timeLeftAccel < 0 :
                timeLeftAccel = 0
                critical = False
                swerve = False
                dataPoint = EndAccelEvent(timeStamp, currentUser, latitude, longitude)

            # Normal Driving
            else:
                dataPoint = GenerateNormalDataPoint(timeStamp, currentUser, latitude, longitude)

            ''' We add to the array each individual dataPoint '''
            dataList.append(dataPoint)

        ''' Bulk Insert '''
        db.session.add_all(dataList)
        db.session.commit()

    return

'''
    This function generates all data for seeding and acts as the intilization point for the seeding program
'''

def GenerateData():

    #just get the current time which we will increment from for the driver
    timeStamp = datetime.today()

    for num in range(NUMOFDAYS):
        print("\nSeeding data for Day {}\n".format(num+1))

        #increment the timeStamp by a day
        timeStamp = timeStamp.today() + timedelta(days=num)
        GenerateDay(timeStamp)


    return

if __name__ == '__main__':
    app = Flask(__name__)
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    except KeyError:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresl@localhost/drivertag'
    db.session.close_all()
    db = SQLAlchemy(app)
    db.reflect()
    db.drop_all()
    db.create_all()

    '''Create fake users'''
    user1 = User('1@test.com', 'Tim Smith')
    user2 = User('2@test.com', 'Matt Smith')
    user3 = User('3@test.com', 'Bob Smith')
    addr = Address("315C Perkins Road", "Rochester", "NY", "14623", "2", "1")
    addr2 = Address("315C Perkins Road", "Rochester", "NY", "14623", "2", "2")
    addr3 = Address("315C Perkins Road", "Rochester", "NY", "14623", "2", "3")
    user1.addr = addr
    user2.addr = addr2
    user3.addr = addr3

    user_array = [user1, user2, user3]
    userArray = [user1, user2]
    db.session.add_all(user_array)
    db.session.commit()
    parse_map_user(user3)

    seedingStartTime = datetime.now()
    GenerateData()
    seedingEndTime = datetime.now()

    db.session.close_all()

    print("\n\n Seeding Completed, it took ", (seedingEndTime-seedingStartTime).total_seconds())




