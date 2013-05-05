from flask import request, redirect, url_for, render_template, abort
from blog import app, rules
from models.entry import Entry


@app.endpoint('index')
def index():
    entries = Entry.objects() 
    return render_template('index.html', entries=entries)

@app.endpoint('read')
def write(url):
    entry = Entry.objects(url=url).first()
    if not entry:
        abort(404)
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
