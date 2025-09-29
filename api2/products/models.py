from mongoengine import Document, StringField, DecimalField, IntField, DateTimeField
from datetime import datetime

class Product(Document):
    MODE_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    ]
    
    name = StringField(max_length=200, required=True)
    price = DecimalField(precision=2, required=True)
    description = StringField(max_length=1000)
    stock_quantity = IntField(default=0)
    mode = StringField(max_length=20, choices=MODE_CHOICES, default='active')
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'products',
        'indexes': ['name', 'price', 'stock_quantity', 'mode', 'created_at']
    }
    
    def __str__(self):
        return self.name
