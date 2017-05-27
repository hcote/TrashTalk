from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY='secretz',
)
app.config.from_object('trashtalk.settings.Development')

# Must import for views to load!
from trashtalk import views
