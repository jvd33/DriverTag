__author__ = 'SWEN356 Team 4'

from app import *
from app.forms import HighRiskTimeForm
from flask_oauthlib.client import OAuth
from flask import render_template, redirect, url_for, session, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user





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
                            request_token_params={'scope': 'email'},
                            )

"""
User loader function
"""


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)

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
    session['name'] = user['name']
    session['email'] = user['email']

    if db.session.query(models.User).filter_by(email=user['email']).one_or_none() is None: #if the user is new
        u = models.User(session['email'], session['name'])
        db.session.add(u)
        db.session.commit()
        flash('You were signed in as %s' % session['name'])
        login_user(u)
        return redirect(url_for('home'))

    u = db.session.query(models.User).filter_by(email=user['email']).one_or_none()
    flash('You were signed in as %s' % session['name'])
    login_user(u)
    return redirect(url_for('home', _external=True))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('oauth_authorized', _external=True))


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('You were successfully logged out.')
    return redirect(url_for('index'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/config', methods=['GET', 'POST'])
@login_required
def user_config():
    form = HighRiskTimeForm()
    if request.method == 'POST' and form.validate():
        hrt = models.HighRiskTime(form.start_time, form.end_time, current_user)
        db.session.add(hrt)
        db.session.commit()
        flash('Time interval added. Be safe out there!')
        return redirect(url_for('config'))

    return render_template('config.html', form=form)