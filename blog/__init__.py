from flask import Flask
from flask_flatpages import FlatPages

app = Flask(__name__)
pages = FlatPages(app)

from blog import views
