from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import schedule
from app.models import *
from flask_mail import Message, Mail
app = Flask(__name__)
mail=Mail(app)


db = SQLAlchemy(app)

def run_every_10_seconds():
    print("Running periodic task!")
    users = User.query.all()
    [email(user) for user in users]

def run_schedule():
    while 1:
        schedule.run_pending()

def email(user):
    msg = Message("Hello",
                  sender="driverTags@gmail.com",
                  recipients=[user.email])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    print(msg)
    mail.send(msg)