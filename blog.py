from __future__ import with_statement
from contextlib import closing

import sqlite3
from delorean import Delorean

from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash

from flask.ext.assets import Environment, Bundle

# configuration
DATABASE = '/tmp/blog.db'
DEBUG = True
SECRET_KEY = '0510'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


assets = Environment(app)

css = Bundle('style.css', filters='cssmin', output="gen/all.css")
assets.register('css_all', css)

import views

if __name__ == '__main__':
    app.run()
