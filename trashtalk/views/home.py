from flask import (Blueprint, current_app, render_template, request,
                   make_response, redirect, url_for, flash)
from flask_login import login_user, login_required, logout_user, current_user

from trashtalk import login_manager
from trashtalk.models import User, db_session
from trashtalk.utils import status
from trashtalk.html_constants import HtmlConstants

html_constants=HtmlConstants()
bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/')
def welcome():
    """Home page. Section is the name of the page in the tab."""
    return render_template("index.html",
                           section='Home')


@bp.route('/error')
def error():
    """Error handling. HTML was never fully built."""
    return render_template('error.html',
                           section="Error")


@bp.route('/signup')
def signup():
    return render_template("register.html",
                           section="Sign up")


@login_manager.unauthorized_handler
def unauthorized_handler():
    """Handle unauthorized access for non-logged in users."""
    flash("Oops! That option is only for registered users")
    return redirect(url_for("signup"), status.HTTP_403_FORBIDDEN)


@login_manager.user_loader
def user_loader(user_id):
    if db_session.query(User).get(user_id):
        user = db_session.query(User).get(user_id)
        current_app.logger.info("Loading user %s", user.get_id())
        return user
    else:
        current_app.logger.info("No user with matching id.")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Website login."""
    username = request.form['username']
    # Check Username exists
    if db_session.query(User).filter(User.username == username).count():
        # Get user account
        user = db_session.query(User).filter(User.username == username).first()
        # Check password against database
        if user.check_password(request.form['password']):
            user.authenticated = True
            db_session.add(user)
            db_session.commit()
            login_user(user, remember=True)  # Reflect user authorization in Flask
            # return redirect(url_for('users.get', user_id=user.id))
            return redirect(url_for("cleanups.get_all"))
        else:
            # Next step: require user feedback password or username incorrect
            flash("Incorrect Username or Password")
            return redirect(url_for("welcome"), code=200)
    else:
        # Next Step: require user feedback password or username incorrect
        flash("Incorrect Username or Password")
        return redirect(url_for("welcome"), code=400)


@bp.route('/logout', methods=["GET"])
@login_required
def logout():
    current_app.logger.info("Logging out ...")
    # Danger of keeping users logged in that don't logout properly
    user = current_user
    user.authenticated = False  # SQL update
    user.save()
    logout_user()  # Flask Update

    return redirect(url_for("welcome"), code=200)


@bp.route('/register', methods=['POST'])
def create_account():
    # TODO: fields for optional inputs: i.e email and volunteer hours
    # Pull data from html form
    new_name = request.form["username"]
    # TODO: Add validator to table to avoid registering unavailable names
    # Check Username exists
    if db_session.query(User).filter(User.username == new_name).count():
        #Send back to try again
        # print("%s is taken" % new_name)
        flash("username: %s, is taken" % new_name)
        return redirect(url_for("signup"), code=status.HTTP_403_FORBIDDEN)
    else:
        #enter password validation process
        new_password = request.form["password"]
        new_confirm_password = request.form["confirm_password"]
        if new_password == new_confirm_password:
            # Create account and log in user
            new_user = User(username=new_name, password=new_password, email=request.form['email'])
            new_user.hash_password()  # Encrypt password
            new_user.authenticated = True  # Login user to SQL
            db_session.add(new_user)
            db_session.commit()
            login_user(new_user, remember=True)  # Login user to Flask
            app.logger.info("%s successfully created an account" % new_name)
            return redirect(url_for('cleanups.get_all'))
        else:
            # Next Step: feedback that passwords do not match
            flash("passwords do not match")
            return redirect(url_for("signup"), code=status.HTTP_403_FORBIDDEN)
