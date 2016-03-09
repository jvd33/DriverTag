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

db.session.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9])
db.session.commit()