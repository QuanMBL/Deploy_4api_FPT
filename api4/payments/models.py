from mongoengine import Document, StringField, DecimalField, DateTimeField
from datetime import datetime

class Payment(Document):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    payment_id = StringField(max_length=100, required=True, unique=True)
    order_id = StringField(max_length=100, required=True)
    amount = DecimalField(precision=2, required=True)
    payment_method = StringField(max_length=20, choices=PAYMENT_METHOD_CHOICES, required=True)
    status = StringField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = StringField(max_length=100)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'payments',
        'indexes': ['payment_id', 'order_id', 'status', 'payment_method', 'created_at']
    }
    
    def __str__(self):
        return f"Payment {self.payment_id}"
