from flask import Blueprint, current_app, render_template, request
from flask import redirect, url_for
from flask_login import login_required
from flask_login import current_user

from geopy.exc import GeopyError

from trashtalk.seeclickfix import postSCFix
from trashtalk.google_sheets import send_to_sheet
from trashtalk.constants import DEFAULT_GEOLOC
from trashtalk.factories import cleanup_factory, location_factory
from trashtalk.models import Cleanup, db_session
from trashtalk.utils import get_location


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
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    return render_template("cleanup/show.html",
                           section="Cleanup",
                           cleanup=cleanups,
                           gmap=current_app.config['GOOGLE_MAPS_ENDPOINT'])


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
                           cleanup=cleanups,
                           section='Create Cleanup')


@cleanup.route('/<int:cleanup_id>', methods=['PUT', 'DELETE'])
def update(cleanup_id):
    """
    Create, update or delete a `Cleanup`

    :param cleanup_id:
    :return: redirects user to cleanups/ or cleanups/:id
    """
    method = request.form['method']
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    if method == 'PUT':
        current_app.logger.debug("REQUEST FORM: %s", request.form)
        cleanups.update(**request.form.to_dict())  # Exceptions handled by models.py
        return redirect(url_for('cleanups.get', cleanup_id=cleanups.id))
    elif method == 'DELETE':
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
    full_address = [request.form['street_number'], request.form['street_name'],
                    DEFAULT_GEOLOC]
    current_app.logger.debug("Address: %s", full_address)
    try:
        geoloc = get_location(full_address)
        location = location_factory(geoloc._asdict())
    except GeopyError:
        db_session.rollback()
        current_app.logger.exception("There was an error finding location.")
    else:
        current_app.logger.debug("Cleanup data: %s", request.form.to_dict())
        cleanup_data = request.form.copy()  # Copy immutable object for editing
        cleanup_data['location'] = location
        cleanup_data['host'] = current_user
        new_cleanup = cleanup_factory(cleanup_data)
        # TODO: Issue #8 - Add condition for using cross street and Google geocoder

        return redirect(url_for('cleanups.get', cleanup_id=new_cleanup.id))
    return redirect(url_for('cleanups.new'))


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
    cleanup_id = request.form['cleanup_id']
    cleanups = db_session.query(Cleanup).get(cleanup_id)
    cleanups.participants.append(current_user)
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
    api_request = postSCFix(
        cleanup)  # Function in SeeClickFix Module,interacts with SeeClickFix API
    response = api_request.json()  # Contains Response from SeeClickFix
    issue_url = response['html_url']  # Important to distinguish site from api urls
    cleanup.html_url = issue_url  # Add to SQL database
    db_session.add(cleanup)
    db_session.commit()
    return redirect(url_for('cleanup', id=id))
  
@cleanup.route('/send_to_pw/<id>')
@login_required
def send_to_pw(id):
    """
    send clean-up data to Public Works google sheet
    :param id:
    :return:
    """
    cleanup = db_session.query(Cleanup).filter(Cleanup.id == id).first()
    host = db_session.query(User).filter(User.id == cleanup.host_id).first()

    num_participants = len(cleanup.participants)
    data = [str(host.username), str(host.email), str(cleanup.start_time), num_participants]
    print(data) #Sanity Check
    send_to_sheet(data) #Very slow function

    return render_template("cleanup/send_to_pw.html",
                           section = 'Send to Public Works')

  
  
