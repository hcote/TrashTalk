from flask import Blueprint, render_template, request
from flask import redirect, url_for
from flask_login import login_required
from flask_login import current_user

from psycopg2 import DataError
from sqlalchemy.exc import DataError

from trashtalk.seeclickfix import postSCFix
from trashtalk import app
from trashtalk.models import Cleanup, User, db_session
from trashtalk.constants import DEFAULT_CITY, DEFAULT_STATE, DEFAULT_GEOLOC
from trashtalk.utils import get_location

cleanup = Blueprint('cleanups', __name__, url_prefix='/cleanups',
                    template_folder='templates', static_folder='../static')


@cleanup.route('/')
def get_all():
    """Display full list of cleanups."""
    try:
        cleanups = db_session.query(Cleanup).all()  # Look at all of the cleanups
    except AttributeError as exc:
        app.logger.error("NullSession, redirecting to homepage")
        return render_template('index.html')
    else:
        return render_template('cleanup/list.html',
                                section="Cleanup",
                                cleanups=cleanups)


@cleanup.route('/<int:cleanup_id>')
def get(cleanup_id):
    """
    Display current clean-up.

    :param cleanup_id:
    :return:
    """
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    return render_template("cleanup/show.html",
                           section="Cleanup",
                           cleanup=cleanups,
                           gmap=app.config['GOOGLE_MAPS_ENDPOINT'])


@cleanup.route('/new')
def new():
    """Return form for creating a new `Cleanup`"""
    return render_template("cleanup/new.html",
                           section="Cleanup",
                           user_id=current_user.id)


@cleanup.route('/<int:cleanup_id>', methods=['POST', 'PUT', 'DELETE'])
def post(cleanup_id):
    method = request.form['method']
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    if method == 'PUT':
        try:
            app.logger.info("REQUEST FORM: %s", request.form)
            cleanups.update(**request.form.to_dict())
        except:
            app.logger.exception("Clean-up update failed.")
        finally:
            return redirect(url_for('cleanups.get', cleanup_id=cleanups.id))
    # TODO: Issue #11 -- Add handling for DELETE Cleanup


@cleanup.route('/create', methods=["POST"])
@login_required
def create():
    """
    POST - Create a new `Cleanup`

    Adds new clean-up and display the new clean-up data. Uses geoPy to find location for events.

    'CITY' can be configured in settings.py

    See SeeClickFix module for info about utility functions used below.

    :return:
    """
    # TODO: Issue #9 - Prevent multiple accidental submissions (ex., when errors occur)
    # TODO: Issue #14 - Implement Location model

    new_date = request.form["date"]
    new_time = request.form['start_time']  # Total hours found through arithmetic
    new_end_time = request.form['end_time']
    new_street_number = request.form['street_number']
    new_street_name = request.form['street_name']
    cross_street_name = request.form['cross_street_name']
    new_image = request.form['image']
    # TODO: Issue #8 - Add condition for using cross street and Google geocoder
    # TODO: geopy requires city and state. Test alternative inputs/outputs and document
    geoloc = get_location(new_street_number, new_street_name, DEFAULT_GEOLOC)
    new_cleanup = Cleanup(date=new_date,
                          start_time=new_time,
                          end_time=new_end_time,
                          street_number=new_street_number,
                          street_name=new_street_name,
                          cross_street_name=cross_street_name,
                          city=geoloc.city,
                          state=geoloc.state,
                          zipcode=geoloc.zipcode,
                          county=geoloc.county,
                          district=geoloc.district,
                          country=geoloc.country,
                          image=new_image,
                          host=current_user,
                          lat=geoloc.latitude,
                          lng=geoloc.longitude,
                          # html_url = issue_url # SeeClick Fix Remnant
                          )
    try:
        new_cleanup.save()
    except DataError:  # add ProgrammingError
        app.logger.exception("New Cleanup not saved. Wrong data type.")
        db_session.rollback()
        raise
    else:
        return redirect(url_for('cleanups.get', cleanup_id=new_cleanup.id))


@cleanup.route('/<int:cleanup_id>/edit')
@login_required
def edit(cleanup_id):
    """
    Update clean-up details.

    :return:
    """
    # TODO: Update form to include current values for current cleanup
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    return render_template('cleanup/edit.html',
                           cleanup=cleanups,
                           section='Create Cleanup')


@cleanup.route('/<int:cleanup_id>/delete', methods=["POST"])
@login_required
def delete(cleanup_id):
    """
    Remove a clean-up. This requires:
        - Remove the relation from the User (`User.cleanups`)
        - Remove all participants from the Cleanup (`Cleanup.participants`)
        - Remove the `Cleanup`

    :param cleanup_id:
    :return:
    """
    # TODO: Notify participants that clean-up was cancelled!
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    # First delete the cleanup from the user's hosting roster
    current_user.cleanups.remove(cleanups)
    # Then, remove all participants from cleanup
    cleanups.participants = []
    # Finally remove the cleanup from SQL
    db_session.delete(cleanups)
    db_session.commit()
    return redirect(url_for('cleanups'))


@cleanup.route('/join', methods=["POST"])
@login_required
def join():
    """
    Users can join currently listed clean-up event.

    :return:
    """
    # TODO: Rename form item to cleanup_id
    cleanup_id = request.form['cleanup_id']
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    cleanups.participants.append(current_user)
    cleanups.save()
    # db_session.add(cleanup)
    # db_session.commit()
    return redirect(url_for('cleanups.get', cleanup_id=cleanups.id))


# RENAME: send_to_scf (seeclickfix)
@cleanup.route('/advertise/<id>')  # ID is from html href/link
@login_required
def advertise_cleanup(id):
    """
    Send clean-up to SeeClickFix.com
    :param id:
    :return:
    """
    cleanup = db_session.query(Cleanup).filter(Cleanup.id == id).first()
    print("Lat: %f, Address: %s" % (cleanup.lat, cleanup.address))  # Sanity Check
    api_request = postSCFix(
        cleanup)  # Function in SeeClickFix Module,interacts with SeeClickFix API
    response = api_request.json()  # Contains Response from SeeClickFix
    issue_url = response['html_url']  # Important to distinguish site from api urls
    cleanup.html_url = issue_url  # Add to SQL database
    db_session.add(cleanup)
    db_session.commit()
    return redirect(url_for('cleanup', id=id))
