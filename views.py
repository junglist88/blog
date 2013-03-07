from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash

from blog import app, db, Entry, User
from werkzeug.routing import Rule

import rules

@app.endpoint('index')
def index():
    entries = Entry.query.limit(4)
    return render_template('index.html', entries=entries)

@app.endpoint('entry.list')
def list_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)

@app.endpoint('entry.read')
def read_entry(id):
    entry = Entry.query.filter_by(id=id).first()
    return render_template('entry.html', entry=entry)

@app.endpoint('entry.add')
def add_entry():
    #if not session.get('logged_in'):
    #    abort(401)
    if request.method == 'POST':
        entry = Entry(request.form['title'], request.form['content'])
        db.session.add(entry)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index'))
    else:
        return render_template('add_entry.html')

@app.endpoint('user.login')
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.endpoint('user.logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
