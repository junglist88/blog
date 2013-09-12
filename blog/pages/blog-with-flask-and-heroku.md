title: Blog with Flask & Heroku
ts: 2012-09-11

Building a markdown formatted blog hosted with
[Flask](http://flask.pocoo.org/) and 
[Heroku](https://www.heroku.com/) is fucking simple.
Most blogging tools on the web today
are attempting to do too many things, require extensive configuration,
or even charge a fee. What you're reading right now was free and took
three simple steps:

    $ vim blog/pages/blog-with-flask-and-heroku.md
    $ git commit -am 'blog with flask and heroku'
    $ git push heroku master

1. Create the new entry.
2. Version my changes.
3. Deploy.

## Setup

> I *highly* recommend that you use virtual environments when working on
> python applications, I use [pythonbrew]() which allows me to create
> individual python installations on my machine.

Go ahead and create a new directory, git repo, and virtualenv.

    $ mkdir blog && cd blog
    $ git init
    $ pythonbrew venv create blog-dev

Lets install our two dependencies. The [flask_flatpages]() package
is used to render our static markdown files:

    $ pip install Flask flask_flatpages

## Code

Next, we need to add 64 lines of code to 4 files.

To blog.py:

    from flask import Flask, render_template
    from flask_flatpages import FlatPages
    from werkzeug.routing import Rule
    from markdown import markdown

    DEBUG = True
    FLATPAGES_AUTO_RELOAD = True
    FLATPAGES_EXTENSION = '.md'

    app = Flask(__name__)
    app.config.from_object(__name__)
    pages = FlatPages(app)

    @app.route('/')
    def index():
        return render_template('index.html', entries=pages)

    @app.route('/<path:path>')
    def entry(path):
        entry = pages.get_or_404(path)
        return render_template('entry.html', entry=entry)

    if __name__ == '__main__':
        app.run()

Now create two folders, one for our templates, and one for our markdown files.

    $ mkdir templates
    $ mkdir pages

Add this to templates/layout.html:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
            <title>{% block title %}{% endblock %}</title>
        </head>
        <body>
            {% block content %}{% endblock %}
        </body>
    </html>

Add this to templates/index.html:

    {% extends "layout.html" %}

    {% block title %}
        Blog
    {% endblock %}

    {% block content %}
        <h1>Entries</h1>
        <ul>
            {% for entry in entries %}
                <li>
                    <a href="{{ url_for('entry', path=entry.path) }}">
                    {{ entry.title }}</a>
                    <small>{{ entry.ts.strftime('%B %e, %Y')  }}</small>
                </li>
            {% endfor %}
        </ul>
    {% endblock %}

Add this to templates/entry.html:

    {% extends "layout.html" %}

    {% block title %}{{ entry.title }}{% endblock %}

    {% block content %}
        <header>
            <h1>{{ entry.title }}</h1>
        </header>
        <article>
            {{ entry.html|safe }}
        </article>
    {% endblock %}

Lets save our progress:

    $ git commit -am 'created flask application'

## Writing your first entry

Create a new markdown file under the pages directory:

    $ touch pages/first-entry.md

Flask-Flatpages uses [YAML]() for the entry metadata. Add this to the new file:

    title: First Blog Entry
    ts: 2013-09-11

    ## This will be rendered as a h2
    Our first blog entry!

Test the app:

    $ python blog.py
    * Running on http://127.0.0.1:5000/
    * Restarting with reloader

## Setting up Heroku

First install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and login:

    $ heroku login

Install [Gunicorn](), the web server:

    $ pip install gunicorn

Create a Procfile so Heroku knows what your app needs run:

    $ echo "web: gunicorn blog:app" | tee -a Procfile

Create a requirements.txt file so Heroku knows what packages your app needs.

    $ pip freeze > requirements.txt

Test the web server:

    $ foreman start

## Deploying

Lets save our progress:

    $ git commit -am 'added procfile'

Create a new git remote so you are able to deploy your app using git push:

    $ heroku create

Deploy:

    $ git push heroku master

Profit:

    $ heroku open
