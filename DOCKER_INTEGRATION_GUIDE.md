# Docker Integration Guide

## Tổng quan
Dự án này sử dụng Docker Compose để quản lý 4 microservices API và MongoDB database. Mỗi API chạy trong container riêng biệt và kết nối với MongoDB container chung.

## Cấu trúc dự án
```
Project_api_test_1/
├── api1/                 # User API (Port 8000)
├── api2/                 # Product API (Port 8001)
├── api3/                 # Order API (Port 8002)
├── api4/                 # Payment API (Port 8003)
├── docker-compose.yml    # Docker Compose configuration
└── mongodb_data/         # MongoDB persistent volume
```

## Cấu hình Docker Compose

### Services được định nghĩa:
1. **user-api**: Django API cho quản lý users
2. **product-api**: Django API cho quản lý products  
3. **order-api**: Django API cho quản lý orders
4. **payment-api**: Django API cho quản lý payments
5. **mongodb**: MongoDB database server

### Network Configuration
- Tất cả services chạy trong network `api-network`
- Các API có thể giao tiếp với nhau thông qua service names
- MongoDB accessible từ tất cả API containers

## Cách sử dụng

### 1. Khởi động toàn bộ dự án
```bash
# Build và start tất cả containers
docker-compose up -d

# Xem logs của tất cả services
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f user-api
```

### 2. Khởi động từng service riêng lẻ
```bash
# Chỉ start MongoDB
docker-compose up -d mongodb

# Start MongoDB + User API
docker-compose up -d mongodb user-api

# Start tất cả API (không bao gồm MongoDB)
docker-compose up -d user-api product-api order-api payment-api
```

### 3. Rebuild containers
```bash
# Rebuild tất cả containers
docker-compose build

# Rebuild container cụ thể
docker-compose build user-api

# Rebuild và restart
docker-compose up -d --build
```

### 4. Dừng và cleanup
```bash
# Dừng tất cả services
docker-compose down

# Dừng và xóa volumes (CẢNH BÁO: Mất data)
docker-compose down -v

# Dừng và xóa images
docker-compose down --rmi all
```

## Truy cập các services

### API Endpoints
- **User API**: http://localhost:8000
- **Product API**: http://localhost:8001
- **Order API**: http://localhost:8002
- **Payment API**: http://localhost:8003

### MongoDB
- **Host**: localhost:27017
- **Username**: admin
- **Password**: password123

## Các lệnh hữu ích

### Kiểm tra trạng thái containers
```bash
# Xem tất cả containers
docker-compose ps

# Xem logs real-time
docker-compose logs -f

# Kiểm tra resource usage
docker stats
```

### Debug containers
```bash
# Vào trong container
docker-compose exec user-api bash
docker-compose exec mongodb mongosh

# Xem logs của container cụ thể
docker-compose logs user-api
docker-compose logs mongodb
```

### Database operations
```bash
# Backup MongoDB
docker-compose exec mongodb mongodump --out /data/backup

# Restore MongoDB
docker-compose exec mongodb mongorestore /data/backup
```

## Xử lý lỗi thường gặp

### 1. Port đã được sử dụng
**Lỗi**: `bind: address already in use`

**Giải pháp**:
```bash
# Kiểm tra process đang sử dụng port
netstat -tulpn | grep :8000

# Kill process
sudo kill -9 <PID>

# Hoặc thay đổi port trong docker-compose.yml
ports:
  - "8001:8000"  # Thay đổi port host
```

### 2. Container không start được
**Lỗi**: `Container keeps restarting`

**Giải pháp**:
```bash
# Xem logs để debug
docker-compose logs user-api

# Kiểm tra health status
docker-compose ps

# Restart container
docker-compose restart user-api
```

### 3. MongoDB connection failed
**Lỗi**: `MongoDB connection timeout`

**Giải pháp**:
```bash
# Kiểm tra MongoDB container
docker-compose logs mongodb

# Test connection
docker-compose exec user-api python -c "import mongoengine; print('MongoDB OK')"

# Restart MongoDB
docker-compose restart mongodb
```

### 4. Volume permission issues
**Lỗi**: `Permission denied` khi write vào volume

**Giải pháp**:
```bash
# Fix permissions
sudo chown -R $USER:$USER ./api1
sudo chmod -R 755 ./api1

# Hoặc chạy với sudo
sudo docker-compose up -d
```

### 5. Out of disk space
**Lỗi**: `No space left on device`

**Giải pháp**:
```bash
# Cleanup unused containers
docker system prune -a

# Cleanup volumes
docker volume prune

# Xem disk usage
docker system df
```

### 6. Network issues
**Lỗi**: `Cannot connect to MongoDB`

**Giải pháp**:
```bash
# Kiểm tra network
docker network ls
docker network inspect project_api_test_1_api-network

# Recreate network
docker-compose down
docker-compose up -d
```

## Environment Variables

### Các biến môi trường quan trọng:
- `MONGODB_HOST`: MongoDB host (default: mongodb)
- `MONGODB_PORT`: MongoDB port (default: 27017)
- `DJANGO_SETTINGS_MODULE`: Django settings module

### Thêm biến môi trường:
```yaml
# Trong docker-compose.yml
environment:
  - DEBUG=True
  - SECRET_KEY=your-secret-key
  - MONGODB_HOST=mongodb
```

## Monitoring và Logs

### Xem logs
```bash
# Logs của tất cả services
docker-compose logs

# Logs với timestamp
docker-compose logs -t

# Logs của service cụ thể
docker-compose logs user-api
```

### Health checks
```bash
# Kiểm tra health status
docker-compose ps

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## Production Deployment

### 1. Sử dụng production settings
```bash
# Set production environment
export DJANGO_SETTINGS_MODULE=userapi.settings_production
docker-compose up -d
```

### 2. Scale services
```bash
# Scale API instances
docker-compose up -d --scale user-api=3
```

### 3. Backup strategy
```bash
# Backup script
#!/bin/bash
docker-compose exec mongodb mongodump --out /data/backup/$(date +%Y%m%d)
docker cp mongodb-container:/data/backup ./backup/
```

## Troubleshooting Commands

```bash
# Kiểm tra tất cả containers
docker ps -a

# Xem resource usage
docker stats

# Kiểm tra network
docker network ls
docker network inspect api-network

# Xem volumes
docker volume ls
docker volume inspect project_api_test_1_mongodb_data

# Cleanup everything
docker-compose down -v --rmi all
docker system prune -a
```

## Best Practices

1. **Luôn sử dụng volumes** cho persistent data
2. **Set restart policies** cho production
3. **Monitor logs** thường xuyên
4. **Backup database** định kỳ
5. **Sử dụng health checks** cho monitoring
6. **Limit resources** để tránh overload
7. **Keep images updated** để bảo mật
