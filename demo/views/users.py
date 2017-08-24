from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from trashtalk import app
from trashtalk.utils import status
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
    user = db_session.query(User).get(user_id)
    return render_template("user/edit.html",
                           user_id=user.id)


@userbp.route('/<int:user_id>', methods=['GET'])
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
        password = request.form['password']
        if  password and (password == request.form['confirm_password']):
            user.update_password(password)
            flash("Password updated")
        email = request.form['email']
        if email:
            user.email = email
            flash("Email updated")
        flash("No other values updated")
        db_session.add(user)
        db_session.commit()
        user = db_session.query(User).get(user_id)
        return render_template("user/show.html",
                               username= user.username,
                               email = user.email)

    elif method == 'POST':
        # create user
        app.logger.info("Create a user ...")
        user = db_session.query(User).get(user_id)
        return render_template("user/show.html",
                               username=user.username,
                               email=user.email)
    elif method == 'DELETE':
        delete(user_id)
        return redirect(url_for("signup"), code=status.HTTP_403_FORBIDDEN)
    else:
        return redirect(url_for("signup"), code=status.HTTP_403_FORBIDDEN)


def delete(user_id):
    """Delete account."""
    user = db_session.query(User).get(user_id).delete()
    db_session.commit()



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
