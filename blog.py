from __future__ import with_statement
from contextlib import closing

import sqlite3
from delorean import Delorean

from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash

from flask.ext.assets import Environment, Bundle

from flask.ext.sqlalchemy import SQLAlchemy

# configuration
DATABASE = '/tmp/blog.db'
DEBUG = True
SECRET_KEY = '0510'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/blog_dev'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

assets = Environment(app)

css = Bundle('style.css', filters='cssmin', output="gen/all.css")
assets.register('css_all', css)

import views

if __name__ == '__main__':
    app.run()
