from flask import request, render_template 
from blog import app, rules, pages
from markdown import markdown
import random

@app.endpoint('index')
def index():
    return render_template('index.html', entries=pages)

@app.endpoint('entry')
def entry(path):
    entry = pages.get_or_404(path)
    return render_template('read.html', entry=entry, entries=pages)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
