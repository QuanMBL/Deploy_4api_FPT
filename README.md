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

### URLs gốc (có thể bị firewall block):
- **User API**: http://localhost:8000
- **Product API**: http://localhost:8001
- **Order API**: http://localhost:8002
- **Payment API**: http://localhost:8003
- **MongoDB**: localhost:27017

### URLs với Port Forwarding (Khuyến nghị):
- **User API**: http://localhost:8081/api/users/
- **Product API**: http://localhost:8080/api/products/
- **Order API**: http://localhost:8082/api/orders/
- **Payment API**: http://localhost:8083/api/payments/

## 🧪 Test API với Postman

### Cấu hình Postman:
- **Headers**: `Content-Type: application/json`
- **Method**: GET hoặc POST
- **URLs**: Sử dụng URLs với Port Forwarding ở trên

### POST Request Bodies:

#### **Product API POST:**
```json
{
    "name": "iPhone 15 Pro",
    "price": "999.99",
    "description": "Latest iPhone with advanced features",
    "stock_quantity": 50,
    "mode": "active"
}
```

#### **User API POST:**
```json
{
    "name": "Nguyen Van A",
    "email": "nguyenvana@example.com"
}
```

#### **Order API POST:**
```json
{
    "order_number": "ORD-001-2024",
    "customer_name": "Nguyen Van A",
    "customer_email": "nguyenvana@example.com",
    "total_amount": "1999.98",
    "status": "pending"
}
```

#### **Payment API POST:**
```json
{
    "payment_id": "PAY-001-2024",
    "order_id": "ORD-001-2024",
    "amount": "1999.98",
    "payment_method": "credit_card",
    "status": "pending",
    "transaction_id": "TXN-123456789"
}
```

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

### Script Test API Tự động
```powershell
# Chạy script test API (Windows PowerShell)
.\test_api_final.ps1

# Hoặc tạo port forwarding và test
docker run -d -p 8080:8001 --network project_api_test_1_api-network --name test-product-api project_api_test_1-product-api
docker run -d -p 8081:8000 --network project_api_test_1_api-network --name test-user-api project_api_test_1-user-api
docker run -d -p 8082:8002 --network project_api_test_1_api-network --name test-order-api project_api_test_1-order-api
docker run -d -p 8083:8003 --network project_api_test_1_api-network --name test-payment-api project_api_test_1-payment-api
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

4. **🚨 VẤN ĐỀ FIREWALL - API KHÔNG THỂ TRUY CẬP TỪ BÊN NGOÀI**

**Triệu chứng:**
- Containers chạy bình thường (`docker-compose ps` hiển thị Up)
- Không thể truy cập API từ browser/Postman
- Lỗi "ERR_EMPTY_RESPONSE" hoặc "socket hang up"
- PowerShell/curl bị block

**Nguyên nhân:**
- Windows Firewall đang block Docker containers
- Docker Desktop Backend có firewall rules BLOCK inbound connections
- Cần quyền admin để tạo firewall rules mới

**Giải pháp:**

**Cách 1: Sử dụng Port Forwarding (Khuyến nghị)**
```bash
# Tạo port forwarding với cùng network
docker run -d -p 8080:8001 --network project_api_test_1_api-network --name test-product-api project_api_test_1-product-api
docker run -d -p 8081:8000 --network project_api_test_1_api-network --name test-user-api project_api_test_1-user-api
docker run -d -p 8082:8002 --network project_api_test_1_api-network --name test-order-api project_api_test_1-order-api
docker run -d -p 8083:8003 --network project_api_test_1_api-network --name test-payment-api project_api_test_1-payment-api
```

**URLs mới để test:**
- Product API: `http://localhost:8080/api/products/`
- User API: `http://localhost:8081/api/users/`
- Order API: `http://localhost:8082/api/orders/`
- Payment API: `http://localhost:8083/api/payments/`

**Cách 2: Tạo Firewall Rules (Cần quyền admin)**
```powershell
# Chạy PowerShell as Administrator
New-NetFirewallRule -DisplayName "Docker API Ports" -Direction Inbound -Protocol TCP -LocalPort 8000,8001,8002,8003 -Action Allow
```

**Cách 3: Sử dụng Browser thay vì Postman**
- Mở browser và truy cập trực tiếp các URLs
- Browser có thể bypass một số firewall restrictions

**Kiểm tra Firewall Rules:**
```powershell
# Xem firewall rules hiện tại
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Docker*"}

# Kiểm tra port có đang mở không
Test-NetConnection -ComputerName localhost -Port 8001
```

**Lưu ý quan trọng:**
- Vấn đề này chỉ xảy ra trên Windows với Docker Desktop
- Linux/macOS thường không gặp vấn đề này
- Port forwarding là giải pháp an toàn nhất

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
