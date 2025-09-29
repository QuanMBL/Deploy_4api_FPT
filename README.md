# 4 Microservices APIs with MongoDB Integration

## 📋 Tổng quan dự án

Dự án này bao gồm 4 microservices API được xây dựng bằng Django và tích hợp với MongoDB, được containerized bằng Docker.

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User API       │    │  Product API    │    │   Order API     │    │  Payment API    │
│   Port: 8000     │    │   Port: 8001    │    │   Port: 8002    │    │   Port: 8003    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         └───────────────────────┼───────────────────────┼───────────────────────┘
                                 │                       │
                    ┌─────────────────────────────────────┐
                    │           MongoDB                    │
                    │         Port: 27017                  │
                    └─────────────────────────────────────┘
```

## 🚀 Các API Services

### 1. User API (Port 8000)
- **Chức năng**: Quản lý người dùng
- **Database**: `userapi_db`
- **Endpoints**: `/users/`, `/users/{id}/`

### 2. Product API (Port 8001)
- **Chức năng**: Quản lý sản phẩm
- **Database**: `productapi_db`
- **Endpoints**: `/products/`, `/products/{id}/`

### 3. Order API (Port 8002)
- **Chức năng**: Quản lý đơn hàng
- **Database**: `orderapi_db`
- **Endpoints**: `/orders/`, `/orders/{id}/`

### 4. Payment API (Port 8003)
- **Chức năng**: Quản lý thanh toán
- **Database**: `paymentapi_db`
- **Endpoints**: `/payments/`, `/payments/{id}/`

## 🛠️ Công nghệ sử dụng

- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: MongoDB 7.0
- **ODM**: MongoEngine 0.27.0
- **Containerization**: Docker + Docker Compose
- **Monitoring**: Django Prometheus
- **CORS**: Django CORS Headers

## 📦 Cài đặt và chạy dự án

### Yêu cầu hệ thống
- Docker
- Docker Compose
- Git

### Các bước cài đặt

1. **Clone repository**
```bash
git clone https://github.com/QuanMBL/Deploy_4api_FPT.git
cd Deploy_4api_FPT
```

2. **Khởi động tất cả services**
```bash
docker-compose up -d
```

3. **Kiểm tra trạng thái**
```bash
docker-compose ps
```

4. **Xem logs**
```bash
docker-compose logs -f
```

## 🌐 Truy cập các services

- **User API**: http://localhost:8000
- **Product API**: http://localhost:8001
- **Order API**: http://localhost:8002
- **Payment API**: http://localhost:8003
- **MongoDB**: localhost:27017

## 📊 Monitoring và Health Checks

### Kiểm tra health của APIs
```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### Kiểm tra MongoDB
```bash
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

## 🔧 Các lệnh hữu ích

### Docker Commands
```bash
# Khởi động services
docker-compose up -d

# Dừng services
docker-compose down

# Rebuild containers
docker-compose build

# Xem logs
docker-compose logs -f [service_name]

# Vào container
docker-compose exec [service_name] bash
```

### MongoDB Commands
```bash
# Kết nối MongoDB
docker-compose exec mongodb mongosh -u admin -p password123

# Backup database
docker-compose exec mongodb mongodump --out /data/backup

# Restore database
docker-compose exec mongodb mongorestore /data/backup
```

## 📁 Cấu trúc dự án

```
Deploy_4api_FPT/
├── api1/                          # User API
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── userapi/
│   └── users/
├── api2/                          # Product API
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── productapi/
│   └── products/
├── api3/                          # Order API
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── orderapi/
│   └── orders/
├── api4/                          # Payment API
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── paymentapi/
│   └── payments/
├── docker-compose.yml             # Docker Compose configuration
├── DOCKER_INTEGRATION_GUIDE.md    # Hướng dẫn Docker
├── MONGODB_INTEGRATION_GUIDE.md   # Hướng dẫn MongoDB
└── README.md                      # File này
```

## 🐛 Troubleshooting

### Lỗi thường gặp và cách khắc phục

1. **Port đã được sử dụng**
```bash
# Kiểm tra process
netstat -tulpn | grep :8000

# Kill process
sudo kill -9 <PID>
```

2. **MongoDB connection failed**
```bash
# Kiểm tra MongoDB container
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

3. **Container không start**
```bash
# Xem logs
docker-compose logs [service_name]

# Rebuild container
docker-compose build [service_name]
```

## 📚 Tài liệu tham khảo

- [Docker Integration Guide](DOCKER_INTEGRATION_GUIDE.md)
- [MongoDB Integration Guide](MONGODB_INTEGRATION_GUIDE.md)

## 🤝 Đóng góp

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 License

Dự án này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm thông tin.

## 👥 Tác giả

- **QuanMBL** - *Initial work* - [QuanMBL](https://github.com/QuanMBL)

## 📞 Liên hệ

Nếu có bất kỳ câu hỏi nào, vui lòng tạo issue trên GitHub repository.
