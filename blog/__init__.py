from flask import Flask
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config.from_object('blog.config')
pages = FlatPages(app)

from blog import views
