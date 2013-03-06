from __future__ import with_statement
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash

from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('locals')
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

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    created_ts = db.Column(db.DateTime)
    content = db.Column(db.Text())

    def __init__(self, title, content):
        from delorean import Delorean
        EST = "US/Eastern"
        d = Delorean(timezone=EST)
        self.title = title
        self.created_ts = d.date
        self.content = content

    def __repr__(self):
        return '<Entry %r>' % self.title

assets = Environment(app)

css = Bundle('style.css', filters='cssmin', output="gen/all.css")
assets.register('css_all', css)

import views

if __name__ == '__main__':
    app.run()
