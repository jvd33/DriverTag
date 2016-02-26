import os

__author__ = 'SWEN356 Team 4'

from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)

app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
)
app.secret_key = '\xa5\x8f\x19\xbb`$\xacw\x91\xe1\xd2\x896R\xf9\x14\x01\xe1\xd5U\xcc\xa9\x13'

from app import views
