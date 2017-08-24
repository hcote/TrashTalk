from flask import Blueprint, current_app, render_template, request, flash
from flask import redirect, url_for
from flask_login import login_required
from flask_login import current_user

from geopy.exc import GeopyError

from trashtalk.seeclickfix import postSCFix
from trashtalk.google_sheets import send_to_sheet
from trashtalk.constants import DEFAULT_CITY, DEFAULT_STATE
from trashtalk.factories import cleanup_factory, location_factory
from trashtalk.models import Cleanup, User, db_session
from trashtalk.utils import get_location#, get_area
from trashtalk.html_constants import HtmlConstants

from trashtalk.input_handling import *

html_constants = HtmlConstants()

cleanup = Blueprint('cleanups', __name__, url_prefix='/cleanups',
                    template_folder='templates', static_folder='../static')

# TODO: Issue #16 - Test refactor with DB connection


@cleanup.route('/')
def get_all():
    """
    Display full list of cleanups.

    :return: list template
    :except: home template
    """
    try:
        cleanups = db_session.query(Cleanup).all()  # Look at all of the cleanups
    except AttributeError:
        current_app.logger.error("NullSession, redirecting to homepage")
        return render_template('index.html')
    else:
        return render_template('cleanup/list.html',
                                section="Cleanup",
                                cleanups=cleanups)


@cleanup.route('/<int:cleanup_id>')
def get(cleanup_id):
    """
    Render current clean-up template.

    :param cleanup_id:
    :return: show template
    """
    # tf = db_session.query(Cleanup).filter(Cleanup.participants.id == current_user.id)
    # tf_two= db_session.query(tf.exists())
    # print("direct_check:", tf_two)

    cleanups = db_session.query(Cleanup).get(cleanup_id)
    bool_participated =check_participants(current_user.id, cleanups.participants)


    return render_template("cleanup/show.html",
                           section="Cleanup",
                           cleanup=cleanups,
                           gmap=current_app.config['GOOGLE_MAPS_ENDPOINT'],
                           start_time = twelve_hour_time(cleanups.start_time),
                           end_time = twelve_hour_time(cleanups.end_time),
                           bool_participated=bool_participated)


@cleanup.route('/new')
def new():
    """
    Render template form for creating a new `Cleanup`. POSTs to cleanups/create

    :return: new template
    """
    return render_template("cleanup/new.html",
                           section="Cleanup",
                           user_id=current_user.id)


@cleanup.route('/<int:cleanup_id>/edit')
@login_required
def edit(cleanup_id):
    """
    Render clean-up editing template. PUTs to cleanups/:id.

    :return: edit template.
    """
    # TODO: Update form to include current values for current cleanup
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    return render_template('cleanup/edit.html',
                           section='Edit Cleanup',
                           id=cleanups.id,
                           date=cleanups.date,
                           current_address=cleanups.location.number,
                           start_time= hour_min_value(cleanups.start_time),
                           start_time_of_day = am_pm_value(cleanups.start_time),
                           end_time = hour_min_value(cleanups.end_time),
                           end_time_of_day = am_pm_value(cleanups.end_time),
                           description=cleanups.description,
                           date_pattern = html_constants.date_pattern,
                           date_placeholder = html_constants.date_placeholder,
                           time_pattern = html_constants.time_pattern,
                           time_placeholder = html_constants.time_placeholder)


@cleanup.route('/<int:cleanup_id>', methods=['POST']) #PUT, 'DELETE'
def update(cleanup_id):
    """
    Create, update or delete a `Cleanup`

    :param cleanup_id:
    :return: redirects user to cleanups/ or cleanups/:id
    """
    cleanup_dict = request.form.to_dict()
    method = cleanup_dict['method']
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    if method == 'POST': #PUT
        current_app.logger.debug("REQUEST FORM: %s", request.form)

        start_time = twenty_four_time(cleanup_dict['start_time'],cleanup_dict['start_time_of_day'])
        end_time = twenty_four_time(cleanup_dict['end_time'],cleanup_dict['end_time_of_day'])
        cleanup_dict.update({"start_time": start_time, "end_time": end_time})

        full_address=get_full_address(cleanup_dict)
        try:
            geoloc = get_location(full_address)
        except:
            current_app.logger.exception("There was an error finding location.")
            flash("s%: Address not found" % full_address)
            return redirect(url_for('cleanups.edit', cleanup_id=cleanup_id))
        else:
            location_dict = {"number": geoloc.address, "latitude": geoloc.latitude, "longitude": geoloc.longitude}
            # edited_dict = edit_dict(request.form.to_dict())
            cleanup_dict.pop("location",None)#Hack- location should be renamed, coming from HTML
            cleanups.update(**cleanup_dict)
            cleanups.location.update(**location_dict)
            return redirect(url_for('cleanups.get', cleanup_id=cleanups.id))

    elif method == 'DELETE':
        print("now deleting")
        cleanups.delete()
        return redirect(url_for('cleanups.get_all'))


@cleanup.route('/create', methods=["POST"])
@login_required
def create():
    """
    POST - Create a new `Cleanup`

    Adds new clean-up and display the new clean-up data. Uses geoPy to find location for
    events. To do that, it must:

        * Parse form for `Location`
        * Parse form for `Cleanup`
        * Send location data via geopy for map coordinates
        * Return map with query to cleanup/:id view

    :return: redirect to cleanup/:id if successful, to cleanup/new if not
    """
    # TODO: Issue #9 - Prevent multiple accidental submissions (ex., when errors occur)
    full_address= get_full_address(request.form.to_dict())
    try:
        geoloc = get_location(full_address)
    except:
        current_app.logger.exception("There was an error finding location.")
        flash("s%: Address not found" % full_address)
        return redirect(url_for('cleanups.new'))
    else:
        location=location_factory(geoloc._asdict())
        cleanup_data = request.form.copy()
        cleanup_data['location']=location
        cleanup_data['host']=current_user
        new_cleanup=cleanup_factory(cleanup_data)
        return redirect(url_for('cleanups.get', cleanup_id=new_cleanup.id))


@cleanup.route('/join', methods=["POST"])
@login_required
def join():
    """
    Users can join currently listed clean-up event.
    :return:
    """
    cleanup_id = request.form['cleanup_id']
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    cleanups.participants.append(current_user)
    cleanups.save()
    return redirect(url_for('cleanups.get', cleanup_id=cleanups.id))


@cleanup.route('/leave', methods=["POST"])
@login_required
def leave():
    """
    Users can join currently listed clean-up event.
    :return:
    """
    cleanup_id = request.form['cleanup_id']
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    cleanups.participants.remove(current_user)
    cleanups.save()
    return redirect(url_for('cleanups.get', cleanup_id=cleanups.id))


@cleanup.route('/advertise/<id>')
@login_required
def send_to_scf(id):
    """
    Send clean-up to SeeClickFix.com
    :param id:
    :return:
    """
    cleanup = db_session.query(Cleanup).filter(Cleanup.id == id).first()
    print("Lat: %f, Address: %s" % (cleanup.lat, cleanup.address))  # Sanity Check
    api_request = postSCFix(cleanup)  # Function in SeeClickFix Module,interacts with SeeClickFix API
    response = api_request.json()  # Contains Response from SeeClickFix
    issue_url = response['html_url']  # Important to distinguish site from api urls
    cleanup.html_url = issue_url  # Add to SQL database
    db_session.add(cleanup)
    db_session.commit()
    return redirect(url_for('cleanup', id=id))


#  Start Coordination with Public Works
@cleanup.route('/send_to_pw/<id>')
@login_required
# Rename to show only starting process
def send_to_pw(id):

    return render_template("cleanup/send_to_pw_really.html",
                           section="Public Works",
                           id=id)


#   Fill out and submit data to Public Works
@cleanup.route('/send_to_pw_really/<id>', methods=["POST"])
@login_required
#Rename to emphasize actually coordination data
def send_to_pw_really(id):
    """
    send clean-up data to Public Works google sheet
    :param id:
    :return:
    """
    tool_data=request.form.copy()
    send_to_sheet(id, tool_data)  # Very slow function
    cleanup = db_session.query(Cleanup).get(id)
    cleanup.notified_pw=True
    db_session.add(cleanup)
    db_session.commit()

    return redirect(url_for('cleanups.get', cleanup_id=id))
    # return render_template("cleanup/show.html",
    #                        section='Send to Public Works')
