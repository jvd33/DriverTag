__author__ = "SWEN356 Team 4"

from wtforms import Form, StringField, validators, IntegerField, DecimalField
import re


def validate_time(form, field):
    regex = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    if bool(regex.match(str(field.data))) is False or field.data == "":
        raise validators.ValidationError("Time must be in format HH:MM")

def validate_zip(form, field):
    if len(field.data) != 5:
        raise validators.ValidationError("Must be a valid zipcode.")

class HighRiskTimeForm(Form):
    start_time = StringField(u'Risk starts at:',
                               [validate_time])
    end_time = StringField(u'Risk ends at:',
                             [validate_time])


class AccelerateForm(Form):
    delta_mph = DecimalField("Change in speed (mph):", [validators.required()])
    seconds = DecimalField("Over interval (seconds)", [validators.required()])


class AddressForm(Form):
    addr = StringField(u'Address:', [validators.required()])
    city = StringField(u'City:', [validators.required()])
    state = StringField(u'State:', [validators.required()])
    zip = StringField(u'Zip Code:', [validators.required()])