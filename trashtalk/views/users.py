from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from trashtalk.utils import status
from trashtalk.models import User, db_session
from trashtalk.html_constants import HtmlConstants

html_constants = HtmlConstants()

bp = Blueprint('users', __name__,
               url_prefix='/users', template_folder='user')


@bp.route('/<int:user_id>/edit', methods=['GET'])
def edit(user_id):
    """
    Route user to a page where they can edit their profile.

    :param user_id:
    :return:
    """
    user = db_session.query(User).get(user_id)
    return render_template("user/edit.html",
                           user_id=user.id,
                           password_pattern = html_constants.password_pattern,
                           password_title =  html_constants.password_title)


@bp.route('/<int:user_id>', methods=['GET'])
def get(user_id):
    """
    Display user profile

    :param user_id:
    :return:
    """
    user = db_session.query(User).get(user_id)
    return render_template("user/show.html",
                           username=user.username,
                           email=user.email)


@bp.route('/<int:user_id>', methods=['POST', 'PUT', 'DELETE'])
def post(user_id):
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
    user = db_session.query(User).get(user_id)
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
        return redirect(url_for("users.get", user_id=user_id),
                        code=status.HTTP_403_FORBIDDEN)

    elif method == 'POST':
        # create user
        current_app.logger.info("Create a user ...")
        return redirect(url_for("users.get", user_id = user_id),
                        code=status.HTTP_403_FORBIDDEN)

    elif method == 'DELETE':
        current_app.logger.info("Create a user ...")
        delete(user_id)
        return redirect(url_for("signup"), code=status.HTTP_403_FORBIDDEN)

    else:
        return redirect(url_for("signup"), code=status.HTTP_403_FORBIDDEN)


def delete(user_id):
    """Delete account."""
    db_session.query(User).get(user_id).delete()
    db_session.commit()


@bp.route('/<int:user_id>/cleanups')
@login_required
def my_cleanups(user_id):
    """
    Display clean-ups created by current user and clean-ups they're participating in.

    :param user_id:
    :return:
    """
    user = db_session.query(User).get(user_id)
    return render_template('user/cleanups.html',
                           # cleanups=user.particpation,
                           my_cleanups=user.cleanups,
                           default_image_path = html_constants.default_image_path)
