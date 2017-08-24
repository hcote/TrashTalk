from flask import render_template

from trashtalk import app
from trashtalk.html_constants import HtmlConstants

from .auth import auth
from .cleanups import cleanup
from .users import userbp

"""
APPLICATION ENDPOINTS

NOTE: HTML *forms* only allow get and post methods. Views using put or delete must
      manually handle those form requests.
"""

# Register routes for users, cleanup and authentication
app.register_blueprint(userbp)
app.register_blueprint(cleanup)
app.register_blueprint(auth)

html_constants = HtmlConstants()


# Public routes (no auth required)
@app.route('/')
def welcome():
    """Home page. Section is the name of the page in the tab."""
    return render_template("index.html",
                           section='Home')


@app.route('/signup')
def signup():
    return render_template("register.html",
                           section="Sign up",
                           password_pattern = html_constants.password_pattern,
                           password_title = html_constants.password_title,
                           username_pattern = html_constants.username_pattern,
                           username_title = html_constants.username_title)
