from flask import request, redirect, url_for, render_template
from blog import app, rules
from models.entry import Entry


@app.endpoint('index')
def index():
    entries = Entry.objects() 
    return render_template('index.html', entries=entries)


@app.endpoint('write')
def write():

    if request.method == 'POST':
        entry = Entry(title=request.form['title'],
                url=request.form['url'],
                text=request.form['text'])
        entry.save()
        return render_template('index.html')

    return render_template('write.html')
