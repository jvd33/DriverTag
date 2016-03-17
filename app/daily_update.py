from flask_sqlalchemy import SQLAlchemy
import schedule
from app.models import *
from flask_mail import Message, Mail
from app import app
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
    print(user.name)
    msg = Message("Hello",
                  sender="driverTags@gmail.com",
                  recipients=[user.email])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    with app.app_context():
        mail.send(msg)