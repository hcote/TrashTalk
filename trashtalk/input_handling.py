# Conversions to handle html inputs; ex) Switch from between 12 and 24hr time


from datetime import *
from trashtalk.constants import DEFAULT_CITY, DEFAULT_STATE


def get_full_address(request_form):
    selection = request_form['location']

    if selection == "current_address":
        full_address = request_form["current_address"]

    if selection=='address':
        full_address = ("%s %s, %s, %s") % (request_form['street_number'], request_form['street_name'], DEFAULT_CITY, DEFAULT_STATE)

    # if selection=='cross_street':
    #     full_address=("%s at %s, %s, %s") % (request_form['street_one'],request_form['street_two'],DEFAULT_CITY, DEFAULT_STATE)

    return full_address


def check_participants(user, participants):
    participant_ids = []
    for participant in participants:
        participant_ids.append(participant.id)
    return user in participant_ids


