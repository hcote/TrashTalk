from flask import Flask

app = Flask(__name__)

# Default configuration is development!
# Override with config.from_envvar('APP_ENV_VAR')
# http://flask.pocoo.org/docs/0.12/config/#configuring-from-files
app.config.from_object('trashtalk.settings.Development')

# Must import for views to load!
from trashtalk import views

# Display user
app.add_url_rule('/users',
                 defaults={'user_id': None},
                 view_func=views.user_view,
                 methods=['GET', 'POST'])
# Show and edit user
# NOTE: HTML *forms* only allow get and post methods. Views using put or delete must
#       manually handle those form requests.
app.add_url_rule('/users/<int:user_id>',
                 view_func=views.user_view,
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
