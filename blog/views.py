from flask import request, render_template 
from blog import app, rules, pages
from markdown import markdown
import random

@app.endpoint('index')
def index():
    entries = [x for x in pages if 'published' in x.meta]
    entries = sorted(entries, reverse=True, key=lambda p: p.meta['published'])
    return render_template('index.html', entries=entries)

@app.endpoint('entry')
def entry(path):
    entry = pages.get_or_404(path)
    return render_template('read.html', entry=entry)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
