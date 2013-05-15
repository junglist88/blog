from blog import app
from werkzeug.routing import Rule

app.url_map.add(Rule('/', endpoint='index'))
app.url_map.add(Rule('/<path:path>', endpoint='entry'))
