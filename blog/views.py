from flask import request, redirect, url_for, render_template, abort
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
