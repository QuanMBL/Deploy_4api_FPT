# MongoDB Integration Guide

## Tổng quan
Dự án sử dụng MongoDB làm database chính cho tất cả 4 microservices. Mỗi API có database riêng biệt và sử dụng MongoEngine ODM để tương tác với MongoDB.

## Cấu hình MongoDB

### Docker Compose Configuration
```yaml
mongodb:
  image: mongo:7.0
  container_name: mongodb-container
  ports:
    - "27017:27017"
  environment:
    - MONGO_INITDB_ROOT_USERNAME=admin
    - MONGO_INITDB_ROOT_PASSWORD=password123
  volumes:
    - mongodb_data:/data/db
  networks:
    - api-network
  restart: unless-stopped
```

### Database Structure
- **userapi_db**: Database cho User API
- **productapi_db**: Database cho Product API  
- **orderapi_db**: Database cho Order API
- **paymentapi_db**: Database cho Payment API

## Cấu hình trong Django Settings

### API1 (Users) - settings.py
```python
# MongoDB configuration using mongoengine
import mongoengine
mongoengine.connect(
    db='userapi_db',
    host=f"mongodb://admin:password123@{os.getenv('MONGODB_HOST', 'mongodb')}:{os.getenv('MONGODB_PORT', '27017')}/"
)
```

### API2 (Products) - settings.py
```python
# MongoDB configuration using mongoengine
import mongoengine
mongoengine.connect(
    db='productapi_db',
    host=f"mongodb://admin:password123@{os.getenv('MONGODB_HOST', 'mongodb')}:{os.getenv('MONGODB_PORT', '27017')}/"
)
```

### API3 (Orders) - settings.py
```python
# MongoDB configuration using mongoengine
import mongoengine
mongoengine.connect(
    db='orderapi_db',
    host=f"mongodb://admin:password123@{os.getenv('MONGODB_HOST', 'mongodb')}:{os.getenv('MONGODB_PORT', '27017')}/"
)
```

### API4 (Payments) - settings.py
```python
# MongoDB configuration using mongoengine
import mongoengine
mongoengine.connect(
    db='paymentapi_db',
    host=f"mongodb://admin:password123@{os.getenv('MONGODB_HOST', 'mongodb')}:{os.getenv('MONGODB_PORT', '27017')}/"
)
```

## Dependencies

### Requirements.txt cho mỗi API
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
gunicorn==21.2.0
mongoengine==0.27.0
pymongo==4.6.0
django-prometheus==2.3.1
psutil==5.9.0
```

## Kết nối MongoDB

### 1. Từ Docker Container
```bash
# Vào MongoDB container
docker-compose exec mongodb mongosh

# Kết nối với authentication
mongosh -u admin -p password123
```

### 2. Từ Host Machine
```bash
# Kết nối từ localhost
mongosh mongodb://admin:password123@localhost:27017/

# Hoặc sử dụng connection string
mongosh "mongodb://admin:password123@localhost:27017/"
```

### 3. Từ Python Code
```python
import mongoengine
from mongoengine import connect

# Kết nối cơ bản
connect('userapi_db', host='mongodb://admin:password123@localhost:27017/')

# Kết nối với options
connect(
    db='userapi_db',
    host='mongodb://admin:password123@localhost:27017/',
    authentication_source='admin'
)
```

## MongoEngine Models

### Ví dụ User Model
```python
from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'email']
    }
```

### Ví dụ Product Model
```python
from mongoengine import Document, StringField, FloatField, IntField, BooleanField

class Product(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    stock_quantity = IntField(default=0)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'products',
        'indexes': ['name', 'is_active']
    }
```

## CRUD Operations

### Create (Thêm mới)
```python
# Tạo user mới
user = User(
    username='john_doe',
    email='john@example.com',
    first_name='John',
    last_name='Doe'
)
user.save()

# Tạo product mới
product = Product(
    name='Laptop',
    description='Gaming laptop',
    price=1500.00,
    stock_quantity=10
)
product.save()
```

### Read (Đọc dữ liệu)
```python
# Lấy tất cả users
users = User.objects.all()

# Lấy user theo username
user = User.objects(username='john_doe').first()

# Lấy products có giá > 1000
expensive_products = Product.objects(price__gt=1000)

# Lấy products đang active
active_products = Product.objects(is_active=True)
```

### Update (Cập nhật)
```python
# Cập nhật user
user = User.objects(username='john_doe').first()
user.first_name = 'Jane'
user.save()

# Cập nhật nhiều records
Product.objects(is_active=False).update(is_active=True)
```

### Delete (Xóa)
```python
# Xóa user
User.objects(username='john_doe').delete()

# Xóa tất cả products không active
Product.objects(is_active=False).delete()
```

## Xử lý lỗi thường gặp

### 1. Connection Error
**Lỗi**: `ServerSelectionTimeoutError`

**Nguyên nhân**: MongoDB container chưa start hoặc network issue

**Giải pháp**:
```bash
# Kiểm tra MongoDB container
docker-compose ps mongodb

# Xem logs MongoDB
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb

# Test connection
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

### 2. Authentication Failed
**Lỗi**: `Authentication failed`

**Nguyên nhân**: Sai username/password hoặc database không tồn tại

**Giải pháp**:
```bash
# Kiểm tra credentials
docker-compose exec mongodb mongosh -u admin -p password123

# Tạo database mới
docker-compose exec mongodb mongosh -u admin -p password123 --eval "use userapi_db"
```

### 3. Database Not Found
**Lỗi**: `Database does not exist`

**Nguyên nhân**: Database chưa được tạo

**Giải pháp**:
```python
# Tạo database trong code
from mongoengine import connect
connect('userapi_db', host='mongodb://admin:password123@localhost:27017/')

# Hoặc tạo thủ công
docker-compose exec mongodb mongosh -u admin -p password123 --eval "use userapi_db; db.createCollection('users')"
```

### 4. Index Error
**Lỗi**: `IndexError: list index out of range`

**Nguyên nhân**: Collection chưa có documents

**Giải pháp**:
```python
# Kiểm tra collection có data không
users = User.objects.count()
if users == 0:
    print("Collection is empty")

# Tạo sample data
User(username='test', email='test@example.com').save()
```

### 5. Validation Error
**Lỗi**: `ValidationError`

**Nguyên nhân**: Dữ liệu không đúng format

**Giải pháp**:
```python
# Kiểm tra validation
try:
    user = User(username='', email='invalid-email')
    user.save()
except ValidationError as e:
    print(f"Validation error: {e}")

# Sửa dữ liệu
user = User(username='valid_user', email='valid@example.com')
user.save()
```

### 6. Connection Pool Exhausted
**Lỗi**: `Connection pool exhausted`

**Nguyên nhân**: Quá nhiều connections

**Giải pháp**:
```python
# Giới hạn connections
from mongoengine import connect
connect(
    db='userapi_db',
    host='mongodb://admin:password123@localhost:27017/',
    maxPoolSize=10,
    minPoolSize=1
)
```

## Monitoring và Debugging

### 1. Kiểm tra kết nối
```bash
# Test connection từ container
docker-compose exec user-api python -c "
import mongoengine
mongoengine.connect('userapi_db', host='mongodb://admin:password123@mongodb:27017/')
print('MongoDB connection successful')
"
```

### 2. Xem database stats
```bash
# Vào MongoDB shell
docker-compose exec mongodb mongosh -u admin -p password123

# Xem databases
show dbs

# Xem collections trong database
use userapi_db
show collections

# Xem stats
db.stats()
```

### 3. Monitor performance
```bash
# Xem active connections
docker-compose exec mongodb mongosh -u admin -p password123 --eval "db.serverStatus().connections"

# Xem operations
docker-compose exec mongodb mongosh -u admin -p password123 --eval "db.serverStatus().opcounters"
```

## Backup và Restore

### 1. Backup Database
```bash
# Backup tất cả databases
docker-compose exec mongodb mongodump --out /data/backup

# Backup database cụ thể
docker-compose exec mongodb mongodump --db userapi_db --out /data/backup

# Copy backup ra host
docker cp mongodb-container:/data/backup ./mongodb-backup
```

### 2. Restore Database
```bash
# Restore từ backup
docker-compose exec mongodb mongorestore /data/backup

# Restore database cụ thể
docker-compose exec mongodb mongorestore --db userapi_db /data/backup/userapi_db
```

### 3. Automated Backup Script
```bash
#!/bin/bash
# backup-mongodb.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/mongodb_$DATE"

# Tạo backup
docker-compose exec mongodb mongodump --out /data/backup_$DATE

# Copy ra host
docker cp mongodb-container:/data/backup_$DATE $BACKUP_DIR

# Nén backup
tar -czf "$BACKUP_DIR.tar.gz" $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup completed: $BACKUP_DIR.tar.gz"
```

## Performance Optimization

### 1. Indexing
```python
# Tạo indexes cho performance
class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    
    meta = {
        'indexes': [
            'username',
            'email',
            ('username', 'email'),  # Compound index
            [('created_at', -1)]    # Descending index
        ]
    }
```

### 2. Connection Pooling
```python
# Cấu hình connection pool
connect(
    db='userapi_db',
    host='mongodb://admin:password123@localhost:27017/',
    maxPoolSize=50,
    minPoolSize=5,
    maxIdleTimeMS=30000
)
```

### 3. Query Optimization
```python
# Sử dụng projection để giảm data transfer
users = User.objects.only('username', 'email')

# Sử dụng limit và skip cho pagination
users = User.objects.skip(10).limit(10)

# Sử dụng select_related cho nested documents
users = User.objects.select_related()
```

## Security Best Practices

### 1. Authentication
```python
# Sử dụng authentication
connect(
    db='userapi_db',
    host='mongodb://username:password@localhost:27017/',
    authentication_source='admin'
)
```

### 2. SSL/TLS
```python
# Kết nối với SSL
connect(
    db='userapi_db',
    host='mongodb://admin:password123@localhost:27017/',
    ssl=True,
    ssl_cert_reqs='CERT_REQUIRED'
)
```

### 3. Environment Variables
```python
# Sử dụng environment variables
import os

MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.getenv('MONGODB_PORT', '27017')
MONGODB_USER = os.getenv('MONGODB_USER', 'admin')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'password123')

connect(
    db='userapi_db',
    host=f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/'
)
```

## Troubleshooting Commands

```bash
# Kiểm tra MongoDB status
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# Xem logs MongoDB
docker-compose logs mongodb

# Kiểm tra connections
docker-compose exec mongodb mongosh -u admin -p password123 --eval "db.serverStatus().connections"

# Xem databases
docker-compose exec mongodb mongosh -u admin -p password123 --eval "show dbs"

# Xem collections
docker-compose exec mongodb mongosh -u admin -p password123 --eval "use userapi_db; show collections"

# Test connection từ API
docker-compose exec user-api python -c "
import mongoengine
try:
    mongoengine.connect('userapi_db', host='mongodb://admin:password123@mongodb:27017/')
    print('MongoDB connection OK')
except Exception as e:
    print(f'MongoDB connection failed: {e}')
"
```

## Production Considerations

1. **Sử dụng replica sets** cho high availability
2. **Enable authentication** và authorization
3. **Setup monitoring** với MongoDB Atlas hoặc tự host
4. **Regular backups** với automated scripts
5. **Performance monitoring** và optimization
6. **Security hardening** với firewall và SSL
7. **Resource limits** cho containers
