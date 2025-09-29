# 📊 Grafana Monitoring Setup Guide

## 🎯 Tổng quan

Hướng dẫn này sẽ giúp bạn triển khai Grafana với dashboard tùy chỉnh để monitor 4 API services (User, Product, Order, Payment) sử dụng Docker Compose.

## 📁 Cấu trúc thư mục

```
📦monitoring
 ┣ 📂grafana
 ┃ ┣ 📂dashboards
 ┃ ┃ ┣ 📜custom_api_dashboard.json
 ┃ ┗ 📂provisioning
 ┃ ┃ ┣ 📂dashboards
 ┃ ┃ ┃ ┗ 📜dashboard.yml
 ┃ ┃ ┗ 📂datasources
 ┃ ┃ ┃ ┗ 📜prometheus.yml
 ┗ 📜prometheus.yml
```

## 🚀 Triển khai

### 1. Khởi động tất cả services

```bash
# Khởi động tất cả services (APIs + MongoDB + Prometheus + Grafana)
docker-compose up -d

# Kiểm tra trạng thái các containers
docker-compose ps
```

### 2. Kiểm tra các services

#### API Services
- **User API**: http://localhost:8000
- **Product API**: http://localhost:8001  
- **Order API**: http://localhost:8002
- **Payment API**: http://localhost:8003

#### Monitoring Services
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

#### Database
- **MongoDB**: localhost:27017

### 3. Kiểm tra Metrics Endpoints

Kiểm tra xem các API có metrics không:

```bash
# User API metrics
curl http://localhost:8000/users/metrics

# Product API metrics  
curl http://localhost:8001/products/metrics

# Order API metrics
curl http://localhost:8002/orders/metrics

# Payment API metrics
curl http://localhost:8003/payments/metrics
```

### 4. Kiểm tra Prometheus

Truy cập http://localhost:9090 và kiểm tra:
- **Status > Targets**: Tất cả APIs phải có status "UP"
- **Graph**: Tìm kiếm metrics như `django_http_requests_total`

## 📊 Cấu hình Grafana

### 1. Đăng nhập Grafana

- **URL**: http://localhost:3000
- **Username**: admin
- **Password**: admin123

### 2. Dashboard tự động

Dashboard tùy chỉnh sẽ được tự động load với các metrics:

#### 📈 Metrics được hiển thị:

1. **📊 Tổng số Services đang hoạt động**
   - Hiển thị số lượng APIs đang chạy
   - Màu sắc thay đổi theo trạng thái

2. **🖥️ CPU Usage trung bình**
   - CPU usage của tất cả APIs
   - Hiển thị dạng phần trăm

3. **💾 Tổng Memory Usage**
   - Tổng memory sử dụng của tất cả APIs
   - Hiển thị dạng bytes

4. **📊 Requests per Second**
   - Số requests/giây cho mỗi API
   - Biểu đồ thời gian thực

5. **✅ Success vs Error Rate**
   - Tỷ lệ thành công vs lỗi
   - Phân biệt 2xx, 4xx, 5xx

6. **💾 Memory Usage by API**
   - Memory sử dụng theo từng API
   - Biểu đồ so sánh

7. **🌐 HTTP Methods by API**
   - Phân tích GET vs POST requests
   - Theo từng API

8. **📊 HTTP Status Codes**
   - Phân bố status codes
   - Stack chart

9. **⏱️ Response Time by API**
   - Thời gian phản hồi
   - Theo từng API

10. **❌ 4xx vs 5xx Errors**
    - Phân biệt client errors vs server errors
    - Theo từng API

11. **🏆 Top APIs by Request Rate**
    - Top 5 APIs có nhiều requests nhất
    - Ranking chart

12. **🖥️ CPU Usage by API**
    - CPU usage chi tiết theo từng API
    - Time series

## 🔧 Cấu hình chi tiết

### Prometheus Configuration

File `monitoring/prometheus.yml` cấu hình:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'user-api'
    static_configs:
      - targets: ['user-api:8000']
    metrics_path: '/users/metrics'
    scrape_interval: 5s

  - job_name: 'product-api'
    static_configs:
      - targets: ['product-api:8001']
    metrics_path: '/products/metrics'
    scrape_interval: 5s

  - job_name: 'order-api'
    static_configs:
      - targets: ['order-api:8002']
    metrics_path: '/orders/metrics'
    scrape_interval: 5s

  - job_name: 'payment-api'
    static_configs:
      - targets: ['payment-api:8003']
    metrics_path: '/payments/metrics'
    scrape_interval: 5s
```

### Grafana Datasource

File `monitoring/grafana/provisioning/datasources/prometheus.yml`:

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

### Dashboard Configuration

File `monitoring/grafana/provisioning/dashboards/dashboard.yml`:

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
```

## 🧪 Test Dashboard

### 1. Tạo traffic test

```bash
# Tạo requests để test metrics
for i in {1..100}; do
  curl -X GET http://localhost:8000/users/ &
  curl -X POST http://localhost:8001/products/ -H "Content-Type: application/json" -d '{"name":"Test Product","price":100}' &
  curl -X GET http://localhost:8002/orders/ &
  curl -X POST http://localhost:8003/payments/ -H "Content-Type: application/json" -d '{"amount":50}' &
done
```

### 2. Kiểm tra metrics trong Prometheus

Truy cập http://localhost:9090 và tìm kiếm:
- `django_http_requests_total`
- `process_cpu_seconds_total`
- `process_resident_memory_bytes`

### 3. Xem dashboard trong Grafana

Truy cập http://localhost:3000 và xem dashboard "Custom API Dashboard - 4 Services Real Data"

## 🛠️ Troubleshooting

### 1. Kiểm tra logs

```bash
# Xem logs của tất cả services
docker-compose logs

# Xem logs của service cụ thể
docker-compose logs grafana
docker-compose logs prometheus
docker-compose logs user-api
```

### 2. Kiểm tra kết nối

```bash
# Kiểm tra Prometheus targets
curl http://localhost:9090/api/v1/targets

# Kiểm tra metrics endpoint
curl http://localhost:8000/users/metrics
```

### 3. Restart services

```bash
# Restart monitoring services
docker-compose restart prometheus grafana

# Restart tất cả
docker-compose restart
```

## 📊 Dashboard Features

### Real-time Metrics
- **Refresh rate**: 30 giây
- **Time range**: 1 giờ (có thể thay đổi)
- **Dark theme**: Tự động áp dụng

### Custom Panels
- **Single Stat**: Hiển thị số liệu quan trọng
- **Graph**: Biểu đồ thời gian thực
- **Stack**: Phân tích chi tiết

### Color Coding
- 🟢 **Green**: Healthy/Good status
- 🟡 **Yellow**: Warning
- 🔴 **Red**: Error/Critical

## 🔄 Cập nhật Dashboard

### 1. Chỉnh sửa dashboard

1. Truy cập Grafana: http://localhost:3000
2. Vào **Dashboards** > **Custom API Dashboard**
3. Click **Settings** > **JSON Model**
4. Chỉnh sửa và **Save**

### 2. Thêm metrics mới

1. Vào **Configuration** > **Data Sources**
2. Chọn **Prometheus**
3. Test connection
4. Thêm panel mới với query PromQL

### 3. Export/Import Dashboard

```bash
# Export dashboard
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:3000/api/dashboards/uid/custom_api_dashboard

# Import dashboard mới
# Copy JSON vào file monitoring/grafana/dashboards/
```

## 🚀 Production Deployment

### 1. Security

```yaml
# Thêm vào docker-compose.yml
environment:
  - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
  - GF_SECURITY_SECRET_KEY=${GRAFANA_SECRET_KEY}
```

### 2. Persistence

```yaml
volumes:
  grafana_data:
    driver: local
  prometheus_data:
    driver: local
```

### 3. Resource Limits

```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '0.5'
    reservations:
      memory: 512M
      cpus: '0.25'
```

## 📈 Monitoring Best Practices

### 1. Alerting Rules

Tạo alerting rules trong Prometheus:

```yaml
# monitoring/alerting_rules.yml
groups:
- name: api_alerts
  rules:
  - alert: HighErrorRate
    expr: rate(django_http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
```

### 2. Retention Policy

```yaml
# Prometheus config
command:
  - '--storage.tsdb.retention.time=30d'
  - '--storage.tsdb.retention.size=10GB'
```

### 3. Backup Strategy

```bash
# Backup Grafana dashboards
docker exec grafana-container grafana-cli admin export-dashboard

# Backup Prometheus data
docker exec prometheus-container tar -czf /backup/prometheus-data.tar.gz /prometheus
```

## 🎯 Kết luận

Với setup này, bạn có:

✅ **Real-time monitoring** cho 4 API services  
✅ **Custom dashboard** với 12 panels chi tiết  
✅ **Prometheus metrics** collection tự động  
✅ **Grafana visualization** đẹp mắt  
✅ **Docker Compose** deployment đơn giản  

Dashboard sẽ hiển thị dữ liệu thực từ các API services, không phải dữ liệu random, giúp bạn monitor hiệu suất và phát hiện vấn đề kịp thời.

---

**🎉 Chúc mừng! Bạn đã setup thành công Grafana monitoring system!**
