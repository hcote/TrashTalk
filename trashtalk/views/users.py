from flask import current_app, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from trashtalk.utils import status
from trashtalk.models import User, db_session
from trashtalk.html_constants import HtmlConstants

html_constants = HtmlConstants()

bp = Blueprint('users', __name__,
               url_prefix='/user', template_folder='user')


@bp.route('/edit', methods=['GET'])
@login_required
def edit():
    """
    Route user to a page where they can edit their profile.

    :param user_id:
    :return:
    """
    try:
        return render_template("user/edit.html",
                        password_pattern=html_constants.password_pattern,
                        password_title=html_constants.password_title)
    except:
        return redirect(url_for("users.get"),
                        code=status.HTTP_403_FORBIDDEN)



@bp.route('/profile', methods=['GET'])
@login_required
def get():
    """
    Display user profile

    :param user_id:
    :return:
    """
    # TODO: Check for user exist, return 404 if not, then update test
    user = db_session.query(User).get(current_user.id)
    try:
        return render_template("user/show.html",
                               username=user.username,
                               email=user.email,
                               code=status.HTTP_200_OK)
    except:
        return render_template("error.html",
                               code=status.HTTP_404_NOT_FOUND)


@bp.route('/', methods=['POST', 'PUT', 'DELETE'])
@login_required
def post():
    """
    Handle put, post and delete requests. HTML forms only provide get and post methods.
    Therefore all forms that are used to modify objects must send a POST and manually
    provide the appropriate method.

    Example:
        <input type="hidden" name="method" value="PUT">

    ...where 'value' is the method to be used for the request.

    :param user_id:
    :return:
    """
    user = db_session.query(User).get(current_user.id)
    method = request.form['method']
    current_app.logger.info("Request method: %s", method)
    if method == 'PUT':
        current_app.logger.info("Process PUT")
        password = request.form['password']
        if password and (password == request.form['confirm_password']):
            user.update_password(request.form['password'])
            flash("Password updated!")
        if request.form['email']:
            user.email = request.form['email']
            flash("Email updated!")
        db_session.add(user)
        db_session.commit()
        return redirect(url_for("users.get"),
                        code=status.HTTP_200_OK)

    elif method == 'POST':
        # create user
        current_app.logger.info("Create user ...")
        return redirect(url_for("users.get"),
                        code=status.HTTP_201_CREATED)

    elif method == 'DELETE':
        current_app.logger.info("Delete user ...")
        delete()
        return redirect(url_for("home.signup"), code=status.HTTP_200_OK)

    else:
        return redirect(url_for("home.signup"), code=status.HTTP_400_BAD_REQUEST)


def delete():
    """Delete account."""
    db_session.query(User).get(current_user.id).delete()
    db_session.commit()


@bp.route('/cleanups')
@login_required
def my_cleanups():
    """
    Display clean-ups created by current user and clean-ups they're participating in.

    :param user_id:
    :return:
    """
    user = db_session.query(User).get(current_user.id)
    return render_template('user/cleanups.html',
                           my_cleanups=user.cleanups,
                           default_image_path = html_constants.default_image_path)
