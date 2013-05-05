import datetime
from mongoengine import connect
from mongoengine import EmbeddedDocument, ObjectIdField, IntField, \
            StringField, DateTimeField, ListField, Document, \
            EmbeddedDocumentField

connect('dev_blog')

class Entry(Document):
    ts = DateTimeField(default=datetime.datetime.utcnow, required=True)
    title = StringField(max_length=200, required=True, unique=True)
    url = StringField(max_length=100, required=True, unique=True)
    text = StringField(required=True)

    meta = {
        'ordering': ['-ts']
    }