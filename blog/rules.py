from blog import app
from werkzeug.routing import Rule

app.url_map.add(Rule('/', endpoint='index'))
app.url_map.add(Rule('/write', endpoint='write'))
app.url_map.add(Rule('/<url>', endpoint='read'))
app.url_map.add(Rule('/edit/<id>', endpoint='edit'))
