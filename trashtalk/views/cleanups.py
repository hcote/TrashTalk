from flask import Blueprint, render_template, request, flash, current_app
from flask import redirect, url_for
from flask_login import login_required
from flask_login import current_user

from geopy.exc import GeopyError

from trashtalk.seeclickfix import postSCFix
from trashtalk.factories import cleanup_factory, location_factory
from trashtalk.models import Cleanup, db_session  # User
from trashtalk.html_constants import HtmlConstants
from trashtalk.input_handling import *
from trashtalk.utils import get_location

html_constants = HtmlConstants()

bp = Blueprint('cleanups', __name__, url_prefix='/cleanups',
               template_folder='templates', static_folder='../static')

# TODO: Issue #16 - Test refactor with DB connection


@bp.route('/')
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
                                cleanups=cleanups,
                                default_image_path = html_constants.default_image_path)


@bp.route('/<int:cleanup_id>')
def get(cleanup_id):
    """
    Render current clean-up template.

    :param cleanup_id:
    :return: show template
    """

    cleanups = db_session.query(Cleanup).get(cleanup_id)
    # Method sort those logged in and out, in reference to participating in cleanups
    if current_user.is_authenticated:
        bool_participated = check_participants(current_user.id, cleanups.participants)
    else:
        bool_participated = False #Default to anonymous users not being participants

    return render_template("cleanup/show.html",
                           section="Cleanup",
                           cleanup=cleanups,
                           gmap=current_app.config['GOOGLE_MAPS_ENDPOINT'],
                           start_time = cleanups.start_time,
                           end_time = cleanups.end_time,
                           bool_participated=bool_participated,
                           default_image_path = html_constants.default_image_path,
                           google_maps_key = '')


@bp.route('/new')
def new():
    """
    Render template form for creating a new `Cleanup`. POSTs to cleanups/create

    :return: new template
    """
    return render_template("cleanup/new.html",
                           section="Cleanup",
                           user_id=current_user.id,
                           date_pattern = html_constants.date_pattern,
                           date_placeholder = html_constants.date_placeholder,
                           time_pattern = html_constants.time_pattern,
                           time_placeholder = html_constants.time_placeholder,
                           text_pattern = html_constants.text_pattern)


@bp.route('/<int:cleanup_id>/edit')
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


@bp.route('/<int:cleanup_id>', methods=['PUT', 'DELETE'])
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
            cleanup_dict.pop("location",None)#Hack- location should be renamed, coming from HTML
            cleanups.update(**cleanup_dict)
            cleanups.location.update(**location_dict)
            return redirect(url_for('cleanups.get', cleanup_id=cleanup_id))

    elif method == 'DELETE':
        print("now deleting")
        cleanups.delete()
        return redirect(url_for('cleanups.get_all'))


@bp.route('/create', methods=["POST"])
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
        if not cleanup_data['image']:
            current_app.logger.info("No image was found: replaced with default")
            cleanup_data['image'] = "crossed_rakes.png"
        else:
            current_app.logger.info("Image found: ", cleanup_data['image'])
        cleanup_data['start_time'] = request.form["start_time"]
        cleanup_data['end_time'] = request.form["end_time"]
        cleanup_data['location'] = location
        cleanup_data['host'] = current_user
        new_cleanup = cleanup_factory(cleanup_data)
        return redirect(url_for('cleanups.get', cleanup_id=new_cleanup.id))


@bp.route('/<int:cleanup_id>/delete', methods=["POST"])
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
    return redirect(url_for('cleanups.get', cleanup_id=cleanup_id))


@bp.route('/join', methods=["POST"])
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
    return redirect(url_for('cleanups.get', cleanup_id=cleanup_id))


@bp.route('/advertise/<id>')
@login_required
def send_to_scf(id):
    """
    Send clean-up to SeeClickFix.com

    :param id:
    :return:
    """
    cleanup = db_session.query(Cleanup).filter(Cleanup.id == id).first()
    current_app.logger.debug("Address: %s" % cleanup.location.number)
    api_request = postSCFix(cleanup)
    response = api_request.json()  # Contains Response from SeeClickFix
    cleanup.html_url = response['html_url']  # Add to SQL Database
    db_session.add(cleanup)
    db_session.commit()
    return redirect(url_for('cleanups.get', cleanup_id=id))


@bp.route('/public_works/<id>', methods=['GET'])
@login_required
def get_public_works(id):
    """
    View Public Works send_password page.

    :param id: cleanup id
    :return:
    """

    return render_template("cleanup/public_works/send.html",
                           section="Public Works",
                           time_placeholder = html_constants.time_placeholder,
                           time_pattern = html_constants.time_pattern,
                           date_placeholder = html_constants.date_placeholder,
                           date_pattern = html_constants.date_pattern,
                           id=id)


@bp.route('/public_works/<id>', methods=["POST"])
@login_required
def send_public_works(id):
    """
    Send cleanup data to Public Works google sheet

    :param id: cleanup id
    :return:
    """
    tool_data=request.form.copy()
    send_to_sheet(id, tool_data)  # Very slow function
    cleanup = db_session.query(Cleanup).get(id)
    cleanup.notified_pw=True
    db_session.add(cleanup)
    db_session.commit()

    return redirect(url_for('cleanups.get', cleanup_id=id))
