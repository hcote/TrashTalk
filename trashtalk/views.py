from flask import render_template, request, make_response
from flask import redirect, url_for
from flask.views import MethodView
from flask_login import LoginManager, login_user, login_required
from flask_login import logout_user, current_user

from trashtalk.seeclickfix import postSCFix, getLocation
from trashtalk import app
from trashtalk.models import Cleanup, User, db_session
from trashtalk.settings import CITY

# Manage Login Feature
login_manager = LoginManager()
login_manager.init_app(app)

# TODO: All status codes should be made constants.


@app.route('/')
def welcome():
    """Home page. Section is the name of the page in the tab."""
    return render_template("home_page.html",
                           section='Home')


@app.route('/error')
def error():
    """Error handling. HTML was never fully built."""
    return render_template('error_display.html',
                           section="Error")


class UserView(MethodView):
    """
    Authenticated views.

    http://flask.pocoo.org/docs/0.12/views/#decorating-views

    Method reference:
        - url_for(view_function, kwargs): Directs to view.
    """

    decorators = [login_required]
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def get(self, user_id):
        """Edit profile form."""
        return render_template("user/edit.html",
                               user=db_session.query(User).get(user_id))

    def post(self, user_id):
        """
        Change profile.

        NOTE: HTML *forms* only allow get and post methods. Views using put or delete
        must manually handle those form requests.
        """
        user = db_session.query(User).get(user_id)
        method = request.form['method']
        app.logger.info("Request method: %s", method)
        if method == 'PUT':
            app.logger.info("Process PUT")
            if request.form['password']:
                user.update_password(request.form['password'])
            if request.form['email']:
                user.email = request.form['email']
            db_session.add(user)
            db_session.commit()
        if method == 'POST':
            # create user
            app.logger.info("Create a user ...")
        if method == 'DELETE':
            self.delete(user_id)
        return render_template("user/show.html",
                               user=db_session.query(User).get(user_id))

    def delete(self, user_id):
        """Delete account."""
        user = db_session.query(User).get(user_id)
        db_session.remove(user)
        db_session.commit()
        return render_template("login.html")

user_view = UserView.as_view('user_view')


@login_manager.unauthorized_handler
def unauthorized_handler():
    """Handle unauthorized access for non-logged in users."""
    return make_response(render_template("unauthorized.html"), 403)


@login_manager.user_loader
def user_loader(user_id):
    user = db_session.query(User).get(user_id)

    app.logger.info("Loading user %s", user.get_id())
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Website login."""
    # pull from html form
    username = request.form['username']
    # Check Username exists
    if db_session.query(User).filter(User.username == username).count():
        # Get user account
        user = db_session.query(User).filter(User.username == username).first()
        # Check password against database
        if user.check_password(request.form['password']):
            user.authenticated = True  # FIXME: Do we still need this?
            db_session.add(user)  # Reflect user authorization in SQL
            db_session.commit()
            login_user(user, remember=True)  # Reflect user authorization in Flask
            return redirect(url_for('user_view', user_id=user.id))
        else:
            # Next step: require user feedback password or username incorrect
            return redirect(url_for("welcome"), code=200)
    else:
        # Next Step: require user feedback password or username incorrect
        return redirect(url_for("welcome"), code=400)


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    # Danger of keeping users logged in that don't logout properly
    user = current_user
    user.authenticated = False  # SQL update
    user.save()
    logout_user()  # Flask Update

    # Next Step: May be better to return to homepage
    return render_template("logout.html",
                           section="Log out")


# PUBLIC ROUTES
@app.route('/signup')
def signup():
    return render_template("enter_user_data.html",
                           section="Sign up")


@app.route('/profile/<username>')
@login_required
def profile(username):
    return render_template("user_profile.html",
                           username=username,
                           section="Profile")


@app.route('/hosted_cleanups')
@login_required
def view_hosted_cleanups():
    return render_template("hosted_cleanups.html",
                           section="Hosted Cleanups")


@app.route('/participated_cleanups')
@login_required
def view_participated_cleanups():
    """Clean-ups a user is participating in."""
    return render_template("participated_cleanups.html",
                           section="Participated Cleanups")


@app.route('/create_account', methods=['POST'])
def create_account():
    # TODO: fields for optional inputs: i.e email and volunteer hours
    # Pull data from html form
    new_name = request.form["username"]
    new_password = request.form["password"]
    new_confirm_password = request.form["confirm_password"]
    # Users can not use unavailable usernames
    # TODO: Add validator to table to avoid registering unavailable names
    if new_password == new_confirm_password:
        # Create account and log in user
        new_user = User(username=new_name, password=new_password)
        new_user.hash_password()  # Encrypt password
        new_user.authenticated = True  # Login user to SQL
        db_session.add(new_user)
        db_session.commit()
        login_user(new_user, remember=True)  # Login user to Flask
        return redirect(url_for('user_view', user_id=new_user.id), code=201)  # Send to profile page
    else:
        # Next Step: feedback that passwords do not match
        return redirect(url_for("signup"), code=403)


@app.route('/cleanup/<id>')
def cleanup(id):
    clean = db_session.query(Cleanup).filter(Cleanup.id == id).first()
    return render_template("cleanup.html",
                           section="Cleanup",
                           clean=clean)


@app.route('/active_clean_ups')
def viewall_cleanup():
    try:
        cleans = db_session.query(Cleanup).all()  # Look at all of the cleanups
    except AttributeError as exc:
        app.logger.error("NullSession, redirecting to homepage")
        return render_template('home_page.html')
    else:
        return render_template('viewall_cleanup.html',
                                section="Active Clean ups",
                                cleans=cleans)


@app.route('/delete_cleanup', methods=["POST"])
@login_required
def delete_cleanup():
    # TODO: Notify participants that clean-up was cancelled!
    cleanup_id = request.form[
        'delete_cleanup_id']  # HTML would only send variables through form.
    cleanup = db_session.query(Cleanup).filter(
        Cleanup.id == cleanup_id).first()  # Object needed to be pulled from SQL, based
    #  on variable
    # Users and cleanups are closley linked by host and participant foreign keys
    # First delete the cleanup from the user's hosting roster
    current_user.cleanups_hosted.remove(cleanup)
    # Then, remove all participants from cleanup
    cleanup.participants = []
    # Finally remove the cleanup from SQL
    db_session.delete(cleanup)
    db_session.commit()
    return redirect(url_for('viewall_cleanup'))


# The logged in user adds him/herself to a selected cleanup
@app.route('/join_cleanup', methods=["POST"])
@login_required
def join_cleanup():
    cleanup_id = request.form['join_cleanup_id']  # HTML would only send variable
    cleanup = db_session.query(Cleanup).filter(
        Cleanup.id == cleanup_id).first()  # From variable, find object from SQL
    cleanup.participants.append(
        current_user)  # User is added via Many-to-Many SQL relationship
    db_session.add(cleanup)
    db_session.commit()
    return redirect(url_for('cleanup', id=cleanup.id))


@app.route('/enter_cleanup_data')
@login_required
def enter_cleanup():
    """Input new clean-up information."""
    return render_template('enter_cleanup_data.html',
                           section='Create Cleanup')


##Add Clean up
##Display the new clean-up data
@app.route('/create_cleanup', methods=["POST"])
@login_required
def create_cleanup():
    """
    Add new clean-up and display the new clean-up data
    :return: 
    """
    # Pull from html form
    new_date = request.form["event_date"]
    new_time = request.form['event_time']  # Total hours found through arithmatic
    new_end_time = request.form['end_time']
    new_street_number = request.form[
        'street_number']  # Next Step: Cross street based location
    new_street_name = request.form['street_name']
    new_image = request.form['event_image']
    location = getLocation(new_street_number, new_street_name,
                           CITY)  # Function lives in 'SeeClickFix' module.
    # Uses geopy to find location
    # City is set at top of page
    # This point once held code to advertise on SeeClickFix immediately after creation
    # The code has since been move to a later stage in the process. However, remnants
    # of the advertisements remain
    new_cleanup = Cleanup(date=new_date,
                          start_time=new_time,
                          end_time=new_end_time,
                          street_number=new_street_number,
                          street_name=new_street_name,
                          image=new_image,
                          host=current_user,
                          lat=location.latitude,
                          lng=location.longitude,
                          address=location.address  # ,
                          # html_url = issue_url # SeeClick Fix Remnant
                          )
    db_session.add(new_cleanup)
    db_session.commit()
    return render_template('create_cleanup.html',
                           section="Confirm Cleanup",
                           cleanup=new_cleanup,
                           url="https://test.seeclickfix.com/issues/1317339"
                           # SeeClickFix Remnant
                           )


@app.route('/advertise/<id>')  # ID is from html href/link
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
