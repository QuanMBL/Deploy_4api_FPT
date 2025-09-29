from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime

class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': ['email', 'created_at']
    }
    
    def __str__(self):
        return self.name
