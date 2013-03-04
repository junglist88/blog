from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash

from delorean import Delorean

from blog import app

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text, ts from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], ts=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/read/<title>')
def read_entry(title):
    cur = g.db.execute('select title, text, ts from entries where title = \'%s\' order by id desc' % title)
    entries = [dict(title=row[0], text=row[1], ts=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    EST = "US/Eastern"
    d = Delorean(timezone=EST)
    g.db.execute('insert into entries (title, text, ts) values (?, ?, ?)',
                 [request.form['title'], request.form['text'], d.date])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
