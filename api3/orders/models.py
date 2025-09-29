from mongoengine import Document, StringField, EmailField, DecimalField, DateTimeField
from datetime import datetime

class Order(Document):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = StringField(max_length=50, required=True, unique=True)
    customer_name = StringField(max_length=100, required=True)
    customer_email = EmailField(required=True)
    total_amount = DecimalField(precision=2, required=True)
    status = StringField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'orders',
        'indexes': ['order_number', 'customer_email', 'status', 'created_at']
    }
    
    def __str__(self):
        return f"Order {self.order_number}"
