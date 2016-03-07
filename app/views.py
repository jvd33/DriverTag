__author__ = 'SWEN356 Team 4'

from app import *
from app import models
from flask_oauthlib.client import OAuth
from flask import render_template, redirect, url_for, session, request, flash, jsonify
from flask_mail import Message, Mail
from celery import Celery
mail=Mail(app)




"""
Defines the OAuth object needed for logging in via Facebook/Google (NYI)
"""
oauth = OAuth(app)
facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key='966689803422128',
                            consumer_secret='5ebcacfed9b216675ed00ff074d87c4b',
                            request_token_params={'scope' : 'email'},
                            )

"""
Gets the current facebook user token, if there is one.
"""


@facebook.tokengetter
def get_fb_token(token=None):
    return session.get('facebook_token')

"""
Handles the oauth response object sent back from Facebook
resp - a dict containing user id and the access token
"""


@app.route('/oauth-authorized')
def oauth_authorized():
    resp = facebook.authorized_response()
    next_url = request.args.get('next') or url_for('index', _external=True)
    if resp is None:
        flash('Your sign in request was denied.')
        return redirect(next_url)
    session['facebook_token'] = (resp['access_token'], '')
    user = facebook.get("/me?fields=id,name,email").data
    session['id'] = user['id']
    session['name'] = user['name']
    session['email'] = user['email']
    u = models.User(session['email'], session['name'])
    db.session.add(u)
    db.session.commit()
    flash('You were signed in as %s' % session['name'])
    return redirect(url_for('home', _external=True))


@app.route('/')
@app.route('/index')
def index():
    if session:
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('oauth_authorized', _external=True))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/home')
def home():
    print(session['email'])
    return render_template('home.html')

@celery.task()
def send_email(email):
    print('made it')
    msg = Message("Hello",
                  sender="driverTags@gmail.com",
                  recipients=[session['email']])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    print(msg)
    mail.send(msg)