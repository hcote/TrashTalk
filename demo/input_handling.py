from datetime import *
from trashtalk.constants import DEFAULT_CITY, DEFAULT_STATE
from trashtalk.utils import get_location
from flask import current_app


def twenty_four_time(hour_min, am_pm):
    twelve = "%s%s" % (hour_min, am_pm)
    t = datetime.strptime(twelve, '%I:%M%p')
    return t.strftime("%H:%M:%S")


def twelve_hour_time(twenty_four):
    t = datetime.strptime(str(twenty_four), '%H:%M:%S')
    return t.strftime('%I:%M%p')


def am_pm_value(twenty_four):
    t = datetime.strptime(str(twenty_four), '%H:%M:%S')
    return t.strftime('%p')


def hour_min_value(twenty_four):
    t = datetime.strptime(str(twenty_four), '%H:%M:%S')
    return t.strftime('%I:%M')


def get_full_address(request_form):
    selection = request_form['location']

    if selection == "current_address":
        full_address = request_form["current_address"]

    if selection=='cross_street':
        full_address=("%s at %s, %s, %s") % (request_form['street_one'],request_form['street_two'],DEFAULT_CITY, DEFAULT_STATE)

    if selection=='address':
        full_address = ("%s %s, %s, %s") % (request_form['street_number'], request_form['street_name'], DEFAULT_CITY, DEFAULT_STATE)

    return full_address


def check_participants(user, participants):
    participant_ids = []
    for participant in participants:
        participant_ids.append(participant.id)
    return user in participant_ids


