from flask import request, redirect, url_for, render_template, abort, flash, session
from blog import app, rules
from models.entry import Entry
from markdown import markdown


@app.endpoint('index')
def index():
    entries = Entry.objects() 
    return render_template('index.html', entries=entries)

@app.endpoint('read')
def read(url):
    entry = Entry.objects(url=url).first()
    if not entry:
        abort(404)
    entry.text = markdown(entry.text, ['codehilite'])
    return render_template('read.html', entry=entry)

@app.endpoint('write')
def write():
    if request.method == 'POST':
        entry = Entry(title=request.form['title'],
                url=request.form['url'],
                text=request.form['text'])
        entry.save()
        return redirect(url_for('index'))

    return render_template('write.html')

@app.endpoint('edit')
def edit(id):
    entry = Entry.objects(id=id).first()
    if not entry:
        abort(404)
    if request.method == 'POST':
        entry.title = request.form['title']
        entry.url = request.form['url']
        entry.text = request.form['text']
        entry.save()
        return redirect(url_for('read', url=entry.url))

    return render_template('edit.html', entry=entry)

@app.endpoint('login')
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username.'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password.'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    if error:
        flash(error)
    return render_template('login.html')

@app.endpoint('logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
