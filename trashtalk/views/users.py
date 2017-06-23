from flask import Blueprint, render_template, request
from flask_login import login_required

from trashtalk import app
from trashtalk.models import User, db_session

userbp = Blueprint('users', __name__,
                   url_prefix='/users', template_folder='user')


@userbp.route('/<int:user_id>/edit', methods=['GET'])
def edit(user_id):
    """
    Route user to a page where they can edit their profile.

    :param user_id:
    :return:
    """
    return render_template("user/edit.html",
                           user=db_session.query(User).get(user_id))


@userbp.route('/<int:user_id>', methods=['GET'])
def get(user_id):
    """
    Display user profile

    :param user_id:
    :return:
    """
    return render_template('user/show.html',
                           user=db_session.query(User).get(user_id))


@userbp.route('/<int:user_id>', methods=['POST', 'PUT', 'DELETE'])
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
        delete(user_id)
    return render_template("user/show.html",
                           user=db_session.query(User).get(user_id))


def delete(user_id):
    """Delete account."""
    user = db_session.query(User).get(user_id)
    db_session.remove(user)
    db_session.commit()
    return render_template("login.html")


@userbp.route('/<int:user_id>/cleanups')
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
                           my_cleanups=user.cleanups)
