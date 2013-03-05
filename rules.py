from blog import app
from werkzeug.routing import Rule

app.url_map.add(Rule('/', endpoint='index'))
app.url_map.add(Rule('/read/<title>', endpoint='entry.read'))
app.url_map.add(Rule('/add', endpoint='entry.add'))
app.url_map.add(Rule('/login', endpoint='user.login'))
app.url_map.add(Rule('/logout', endpoint='user.logout'))