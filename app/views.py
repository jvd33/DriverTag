__author__ = 'SWEN356 Team 4'

from app import *
from app.forms import HighRiskTimeForm, AccelerateForm, AddressForm
from flask_oauthlib.client import OAuth
from flask import render_template, redirect, url_for, session, request, flash, json
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import requests



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
    addr = db.session.query(models.Address).filter_by(user_id=current_user.id).one_or_none()

    return render_template('config.html', form1=HighRiskTimeForm(),
                           form2=AccelerateForm(), form3=AddressForm(),
                           times=times, accel=accel, addr=addr, jsname="config.js")


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
Getting Information for High Risk Times
"""


@app.route('/hrreport/<id_user>')
@login_required
def high_risk_report(id_user):
    user = models.User.query.filter_by(id=id_user).first()
    times = db.session.query(models.HighRiskTime).filter_by(user_id=id_user).all()
    user_info = list()
    if id_user and user:
        dataList = user.data.all()
        for data in dataList:
            for t in times:
                if data.timestamp>=t.start_time and data.timestamp<=t.end_time:
                    user_info.append(data)
        return render_template('dailyreports_hr.html', datas=user_info)

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


@app.route('/daily_report/<user_id>')
@login_required
def daily_report(user_id):

    fake_user = models.User.query.filter_by(id=user_id).first()

    x_accel = []
    y_accel = []
    z_accel = []
    timestamps = []

    if user_id and fake_user:
        dataList = fake_user.data.all()

        #format the acceleration down to 6 decimal places
        for data in dataList:
            data.x_accelorometer = round(data.x_accelorometer,6)
            data.y_accelorometer = round(data.y_accelorometer,6)
            data.z_accelorometer = round(data.z_accelorometer,6)
            x_accel.append(data.x_accelorometer)
            y_accel.append(data.y_accelorometer)
            z_accel.append(data.z_accelorometer)
            timestamps.append(str(data.timestamp))

        xaccel_string = [float(i) for i in x_accel]
        points = list(zip(timestamps, xaccel_string)) # data for highcharts must be [ [x, y], [x, y],...]
        yaccel_string = [str(i) for i in y_accel]

        return render_template('dailyReport.html', datas=dataList ,x_accel=points, y_accel=yaccel_string, z_accel=z_accel, timestamps=timestamps)
    return redirect(url_for('home'))

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

"""
Map page view
"""


@app.route('/map/<user_id>')
@login_required
def map_page(user_id):
    key = "AIzaSyBp_559TLwKdvOGuvtaryHmolJnbBpOuk0" # google api key
    user = models.User.query.filter_by(id=current_user.id).first()
    if user.addr:
        address = "%s %s %s %s" % (user.addr.street, user.addr.city, user.addr.state, user.addr.zip)
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&components=country:US&key=%s" % (address, key)

        response = json.loads(requests.get(url).content)
        addlat = response['results'][0]['geometry']['location']['lat']
        addlng = response['results'][0]['geometry']['location']['lng']
        r = user.addr.radius

        return render_template('map.html', addr=True, addlat=addlat, addlng=addlng, radius=r)
    return render_template('map.html', addr=False, addlat=0, addlng=0, radius=0)

"""
User address input
"""


@app.route('/address', methods=['POST'])
@login_required
def address():
    form = AddressForm(request.form)
    addr = models.User.query.filter_by(id=current_user.id).first().addr

    if form.validate() and not addr:
        print(form.zip.data)
        new = models.Address(
            form.addr.data,
            form.city.data,
            form.state.data,
            form.zip.data,
            form.radius.data,
            current_user.id
        )
        db.session.add(new)
        db.session.commit()
        flash('Address added!')
    else:
        flash('You can only have one address.')

    return redirect(url_for('user_config'))

"""
Address deletion
"""


@app.route('/address/delete/')
@login_required
def del_addr():
    address = models.User.query.filter_by(id=current_user.id).first().addr
    if address:
        db.session.delete(address)
        db.session.commit()
        flash("Acceleration threshold deleted.")
    return redirect(url_for('user_config'))
