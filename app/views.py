__author__ = 'SWEN356 Team 4'

from app import *
from app.forms import HighRiskTimeForm, AccelerateForm
from flask_oauthlib.client import OAuth
from flask import render_template, redirect, url_for, session, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, time





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
Redirects to index if user is not logged in
"""


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('index'))

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
    if current_user.is_active:
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('oauth_authorized', _external=True))


@app.route('/logout')
@login_required
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

    # gets all the user's unique high risk times for display
    times = db.session.query(models.HighRiskTime).filter_by(user=current_user)\
        .distinct(models.HighRiskTime.start_time).distinct(models.HighRiskTime.end_time).all()

    accel = db.session.query(models.Acceleration).filter_by(user_id=current_user.id).one_or_none()

    return render_template('config.html', form1=HighRiskTimeForm(),
                           form2=AccelerateForm(), times=times, accel=accel)


"""
High Risk Time form handler
"""


@app.route('/hrt', methods=['POST'])
@login_required
def hrt():
    form = HighRiskTimeForm(request.form)
    if form.validate():

        start = datetime.strptime(form.start_time.data, "%H:%M")
        end = datetime.strptime(form.end_time.data, "%H:%M")
        time = db.session.query(models.HighRiskTime).filter_by(user=current_user).all()
        highrisk = models.HighRiskTime(start, end, current_user.id)

        # if this time interval isnt unique, add it to the db
        if (highrisk.start_time, highrisk.end_time) not in {t.start_time: t.end_time for t in time}.items():
            db.session.add(highrisk)
            db.session.commit()
            flash('Time interval added. Be safe out there!')
        else:
            flash('Time interval already added.')

    return redirect(url_for('user_config'))

"""
High Risk Time deletion
"""


@app.route('/hrt/delete/<hrt_id>')
@login_required
def delete_hrt(hrt_id):
    hrt = models.HighRiskTime.query.filter_by(id=hrt_id).one_or_none()
    if hrt:
        db.session.delete(hrt)
        db.session.commit()
        flash("High risk time interval deleted.")
    return redirect(url_for('user_config'))


"""
Acceleration form handler
"""


@app.route('/accel', methods=['POST'])
@login_required
def accel():
    form = AccelerateForm(request.form)
    accel = models.User.query.filter_by(id=current_user.id).first().accel

    if form.validate() and not accel:
        acc = models.Acceleration(form.delta_mph.data, form.seconds.data, current_user.id)
        db.session.add(acc)
        db.session.commit()
        flash('Acceleration threshold added!')
    else:
        flash('You can only have one acceleration threshold.')

    return redirect(url_for('user_config'))

"""
Acceleration deletion
"""


@app.route('/accel/delete/')
@login_required
def del_accel():
    accel = models.User.query.filter_by(id=current_user.id).first().accel
    if accel:
        db.session.delete(accel)
        db.session.commit()
        flash("Acceleration threshold deleted.")
    return redirect(url_for('user_config'))

