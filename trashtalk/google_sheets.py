#Sheets API Requires a Google Cloud services account.
#Instructions are found in this link
#http://gspread.readthedocs.io/en/latest/oauth2.html


import gspread
import datetime

from trashtalk.models import Cleanup, db_session
from oauth2client.service_account import ServiceAccountCredentials
from flask import current_app

GOOGLE_SHEETS_VALIDATION = current_app.config['GOOGLE_SHEETS_VALIDATION']
GOOGLE_SHEETS_SCOPE = current_app.config['GOOGLE_SHEETS_SCOPE']
GOOGLE_SHEETS_KEY = current_app.config['GOOGLE_SHEETS_KEY']

top_row = 2 #First Row is header: Limited ability to find the end of the data. Easier just to put data at the top and find it later

credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_VALIDATION, GOOGLE_SHEETS_SCOPE)
gc = gspread.authorize(credentials)
wks = gc.open_by_key(GOOGLE_SHEETS_KEY).sheet1


# Function used in cleanups.py for send_to_pw_really.html
def send_to_sheet(id, tool_data):
    cleanup = db_session.query(Cleanup).filter(Cleanup.id == id).first()
    #TODO: Match data format of Public Works
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    legal_name=tool_data.get('legal_name')
    home_address = tool_data.get('home_address')
    email = tool_data.get('email')
    phone_number = tool_data.get("phone_number")

    cleanup_address=cleanup.location.address
    num_participants = len(cleanup.participants) + 1
    cleanup_date = cleanup.date
    start_end_times = '%s - %s' % (cleanup.start_time, cleanup.end_time)

    staff_contact = tool_data.get("staff_contact")
    tool_pickup_date=tool_data.get("tool_pickup_date")
    tool_pickup_time=tool_data.get("tool_pickup_time")
    pickup_time_of_day=tool_data.get("pickup_time_of_day")
    tool_pickup = "%s, %s %s" %(tool_pickup_date, tool_pickup_time, pickup_time_of_day)

    tool_drop_off_date=tool_data.get("tool_drop_off_date")
    tool_drop_off_time=tool_data.get("tool_drop_off_time")
    drop_off_time_of_day=tool_data.get("drop_off_time_of_day")
    tool_drop_off = "%s, %s %s" % (tool_drop_off_date, tool_drop_off_time, drop_off_time_of_day)

    # tools
    empty=0
    rubber_dipped=tool_data.get("rubber_dipped")
    small_nitrile=tool_data.get("small_nitrile")
    medium_nitrile=tool_data.get("medium_nitrile")
    large_nitrile=tool_data.get("large_nitrile")
    cotton_glove=tool_data.get("cotton_glove")
    vest=tool_data.get("vest")
    regular_pick_stick=tool_data.get("regular_pickup_stick")
    small_pick_stick=tool_data.get("small_pickup_stick")
    push_broom=tool_data.get("push_broom")
    reg_house_broom=tool_data.get("reg_house_broom")
    small_house_broom=tool_data.get('small_house_broom')
    reg_dust_pan=tool_data.get("reg_dust_pan")
    long_handle_dust_pan=tool_data.get("long_handle_dust_pan")
    paint=empty
    hand_clippers = tool_data.get("hand_clippers")
    loppers = tool_data.get("loppers")
    pruning_saw = tool_data.get("pruning_saw")
    shears = tool_data.get("shears")
    held_bulb_planter = tool_data.get("held_bulb_planter")
    long_bulb_planter = tool_data.get("long_bulb_planter")
    hand_hoe=tool_data.get("hand_hoe")
    hand_trowel=tool_data.get("hand_trowel")
    hand_weeder=tool_data.get("hand_weeder")
    hori_hori = tool_data.get("hori_hori")
    mattock_tiller=tool_data.get("mattock_tiller")
    fifteen_mattock=tool_data.get("fifteen_mattock")
    twenty_three_mattock = tool_data.get("twenty_three_mattock")
    thirty_two_mattock=tool_data.get("thirty_two_mattock")
    pick_ax =tool_data.get("pick_ax")
    fire_ax=tool_data.get("fire_ax")
    standard_hoe = tool_data.get("standard_hoe")
    hula_hoe = tool_data.get("hula_hoe")
    standard_leaf_rake = tool_data.get("standard_leaf_rake")
    narrow_leaf_rake=tool_data.get("narrow_leaf_rake")
    bow_rake = tool_data.get("bow_rake")
    pitch_fork = tool_data.get("pitch_fork")
    mcleod=tool_data.get("mcleod")
    pointed_shovel=tool_data.get("pointed_shovel")
    flat_shovel = tool_data.get("flat_shovel")
    scoop_shovel=tool_data.get("scoop_shovel")
    grass_trimmers=tool_data.get("grass_trimmers")
    standard_weed_wrench=tool_data.get("standard_weed_wrench")
    large_weed_wrench=tool_data.get("large_weed_wrench")
    plastic_bag=tool_data.get("plastic_bag")
    green_waste=tool_data.get("green_waste")
    reusable_bag=tool_data.get("reusable_bag")
    first_aid = tool_data.get("first_aid")
    cooler=tool_data.get("cooler")
    five_gal_buck=tool_data.get("five_gal_buck")
    two_gal_buck = tool_data.get("two_gal_buck")
    skimmer=tool_data.get("skimmer")
    ed_poster=empty
    other=empty

    formatted_data = [timestamp, legal_name, home_address, email, phone_number, cleanup_address, "Illegal Dumping",
                      num_participants, cleanup_date, start_end_times, "Debris Plan", tool_pickup, tool_drop_off,
                      staff_contact,rubber_dipped, small_nitrile, medium_nitrile, large_nitrile, cotton_glove, vest,
                      regular_pick_stick, small_pick_stick, push_broom, reg_house_broom, small_house_broom, reg_dust_pan,
                      long_handle_dust_pan, paint, paint, paint, paint, paint, paint, paint, paint, paint, paint, paint,
                      paint, paint, hand_clippers, loppers,pruning_saw,shears,held_bulb_planter,long_bulb_planter,
                      hand_hoe,hand_trowel,hand_weeder,hori_hori, mattock_tiller,fifteen_mattock,twenty_three_mattock,
                      thirty_two_mattock,pick_ax,fire_ax,standard_hoe,hula_hoe,standard_leaf_rake,narrow_leaf_rake,
                      bow_rake,pitch_fork,mcleod,pointed_shovel,flat_shovel,scoop_shovel,grass_trimmers,
                      standard_weed_wrench,large_weed_wrench,plastic_bag,green_waste,reusable_bag,first_aid,cooler,
                      five_gal_buck,two_gal_buck,skimmer, ed_poster, other]

    wks.insert_row(formatted_data,index=top_row)
