# 📊 Kibana Logging Setup Guide

## 🎯 Tổng quan

Hướng dẫn này sẽ giúp bạn triển khai ELK Stack (Elasticsearch, Logstash, Kibana) để monitor và phân tích logs từ 4 API services sử dụng Docker Compose.

## 📁 Cấu trúc thư mục

```
📦logging
 ┣ 📂elasticsearch
 ┃ ┗ 📜elasticsearch.yml
 ┣ 📂kibana
 ┃ ┣ 📜kibana.yml
 ┃ ┗ 📜api-dashboard.json
 ┣ 📂logstash
 ┃ ┣ 📂config
 ┃ ┃ ┗ 📜logstash.yml
 ┃ ┗ 📂pipeline
 ┃ ┃ ┣ 📜api-logs.conf
 ┃ ┃ ┗ 📜logstash.conf
 ┣ 📜django_logging.py
 ┗ 📜logstash_middleware.py
```

## 🚀 Triển khai

### 1. Khởi động ELK Stack

```bash
# Khởi động tất cả services (APIs + MongoDB + Prometheus + Grafana + ELK)
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

#### Logging Services
- **Elasticsearch**: http://localhost:9200
- **Kibana**: http://localhost:5601

#### Database
- **MongoDB**: localhost:27017

### 3. Kiểm tra Elasticsearch

```bash
# Kiểm tra Elasticsearch health
curl http://localhost:9200/_cluster/health

# Kiểm tra indices
curl http://localhost:9200/_cat/indices
```

### 4. Kiểm tra Logstash

```bash
# Kiểm tra Logstash logs
docker-compose logs logstash

# Test gửi log tới Logstash
echo '{"message": "test log", "service": "test-api"}' | nc localhost 5000
```

## 📊 Cấu hình Kibana

### 1. Truy cập Kibana

- **URL**: http://localhost:5601
- **Không cần đăng nhập** (security disabled)

### 2. Tạo Index Pattern

1. Vào **Stack Management** > **Index Patterns**
2. Click **Create index pattern**
3. Nhập pattern: `api-logs-*`
4. Chọn time field: `@timestamp`
5. Click **Create index pattern**

### 3. Import Dashboard

1. Vào **Stack Management** > **Saved Objects**
2. Click **Import**
3. Upload file `logging/kibana/api-dashboard.json`
4. Click **Import**

### 4. Xem Dashboard

1. Vào **Dashboard**
2. Chọn **API Logs Dashboard**
3. Xem các metrics:
   - **API Requests Over Time**: Biểu đồ requests theo thời gian
   - **Response Status Codes**: Phân bố status codes
   - **Top Services by Request Count**: Top services có nhiều requests
   - **Average Response Time by Service**: Thời gian phản hồi trung bình
   - **Recent API Logs**: Bảng logs gần đây

## 🔧 Cấu hình chi tiết

### Elasticsearch Configuration

File `logging/elasticsearch/elasticsearch.yml`:

```yaml
cluster.name: "api-cluster"
node.name: "api-node-1"
network.host: 0.0.0.0
discovery.type: single-node
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
xpack.security.http.ssl.enabled: false
xpack.security.transport.ssl.enabled: false
xpack.monitoring.collection.enabled: true
```

### Kibana Configuration

File `logging/kibana/kibana.yml`:

```yaml
server.name: kibana
server.host: "0.0.0.0"
elasticsearch.hosts: [ "http://elasticsearch:9200" ]
monitoring.ui.container.elasticsearch.enabled: true
xpack.security.enabled: false
xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters_long"
```

### Logstash Configuration

File `logging/logstash/pipeline/api-logs.conf`:

```ruby
input {
  beats {
    port => 5044
  }
  
  tcp {
    port => 5000
    codec => json_lines
  }
  
  udp {
    port => 5000
    codec => json_lines
  }
}

filter {
  if [fields][service] {
    mutate {
      add_field => { "service_name" => "%{[fields][service]}" }
    }
  }
  
  # Parse Django logs
  if [message] =~ /\[.*\]/ {
    grok {
      match => { "message" => "\[%{TIMESTAMP_ISO8601:timestamp}\] \[%{NUMBER:pid}\] \[%{LOGLEVEL:level}\] %{GREEDYDATA:log_message}" }
    }
  }
  
  # Parse HTTP request logs
  if [message] =~ /HTTP/ {
    grok {
      match => { "message" => "%{IPORHOST:client_ip} - - \[%{HTTPDATE:timestamp}\] \"%{WORD:method} %{URIPATH:request_path}(?:%{URIPARAM:request_params})? %{DATA:http_version}\" %{NUMBER:response_code} %{NUMBER:response_size}" }
    }
  }
  
  # Add timestamp
  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "api-logs-%{+YYYY.MM.dd}"
  }
  
  stdout {
    codec => rubydebug
  }
}
```

## 🔌 Tích hợp với Django APIs

### 1. Cập nhật Django Settings

Thêm vào `settings.py` của mỗi API:

```python
# Import logging configuration
from logging_django_logstash import LOGGING

# Add to settings
LOGGING = LOGGING

# Add middleware
MIDDLEWARE = [
    'logging_django_logstash.LogstashMiddleware',
    # ... other middleware
]
```

### 2. Cài đặt dependencies

Thêm vào `requirements.txt`:

```
elasticsearch==8.11.0
```

### 3. Tạo logs directory

```bash
# Trong mỗi API container
mkdir -p /app/logs
```

## 🧪 Test Logging System

### 1. Tạo traffic test

```bash
# Tạo requests để test logging
for i in {1..50}; do
  curl http://localhost:8000/api/users/ &
  curl http://localhost:8001/api/products/ &
  curl http://localhost:8002/api/orders/ &
  curl http://localhost:8003/api/payments/ &
  sleep 1
done
```

### 2. Kiểm tra logs trong Elasticsearch

```bash
# Kiểm tra indices
curl http://localhost:9200/_cat/indices

# Xem logs mới nhất
curl -X GET "localhost:9200/api-logs-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "size": 10
}'
```

### 3. Xem logs trong Kibana

1. Truy cập http://localhost:5601
2. Vào **Discover**
3. Chọn index pattern `api-logs-*`
4. Xem logs real-time

## 📊 Dashboard Features

### Real-time Log Analysis
- **Time range**: Tự động cập nhật
- **Refresh rate**: Real-time
- **Filters**: Theo service, status code, method

### Custom Visualizations
- **Line Chart**: Requests over time
- **Pie Chart**: Status codes distribution
- **Bar Chart**: Top services
- **Table**: Recent logs with details

### Log Fields Available
- `@timestamp`: Thời gian log
- `service`: Tên service (user-api, product-api, etc.)
- `level`: Log level (INFO, ERROR, WARNING)
- `message`: Nội dung log
- `http.method`: HTTP method (GET, POST, etc.)
- `http.status_code`: Status code
- `http.path`: Request path
- `performance.duration_ms`: Response time
- `client_ip`: Client IP address

## 🔍 Advanced Queries

### 1. Tìm logs lỗi

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "http.status_code": {
              "gte": 400
            }
          }
        }
      ]
    }
  }
}
```

### 2. Tìm logs theo service

```json
{
  "query": {
    "term": {
      "service": "user-api"
    }
  }
}
```

### 3. Tìm logs chậm

```json
{
  "query": {
    "range": {
      "performance.duration_ms": {
        "gte": 1000
      }
    }
  }
}
```

## 🛠️ Troubleshooting

### 1. Kiểm tra logs

```bash
# Xem logs của tất cả services
docker-compose logs

# Xem logs của service cụ thể
docker-compose logs elasticsearch
docker-compose logs kibana
docker-compose logs logstash
```

### 2. Kiểm tra kết nối

```bash
# Kiểm tra Elasticsearch
curl http://localhost:9200/_cluster/health

# Kiểm tra Kibana
curl http://localhost:5601/api/status

# Test Logstash
echo '{"test": "message"}' | nc localhost 5000
```

### 3. Restart services

```bash
# Restart ELK stack
docker-compose restart elasticsearch kibana logstash

# Restart tất cả
docker-compose restart
```

## 📈 Performance Optimization

### 1. Elasticsearch Tuning

```yaml
# Thêm vào docker-compose.yml
environment:
  - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
  - discovery.type=single-node
  - xpack.security.enabled=false
```

### 2. Logstash Tuning

```yaml
# Thêm vào docker-compose.yml
environment:
  - "LS_JAVA_OPTS=-Xmx512m -Xms512m"
```

### 3. Index Management

```bash
# Tạo index template
curl -X PUT "localhost:9200/_index_template/api-logs" -H 'Content-Type: application/json' -d'
{
  "index_patterns": ["api-logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }
}'
```

## 🔄 Log Rotation

### 1. Elasticsearch Index Lifecycle

```bash
# Tạo lifecycle policy
curl -X PUT "localhost:9200/_ilm/policy/api-logs-policy" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "1GB",
            "max_age": "7d"
          }
        }
      },
      "delete": {
        "min_age": "30d"
      }
    }
  }
}'
```

### 2. Logstash Buffer

```ruby
# Thêm vào logstash.conf
input {
  tcp {
    port => 5000
    codec => json_lines
    buffer_size => 8192
  }
}
```

## 🎯 Kết luận

Với setup này, bạn có:

✅ **Real-time logging** cho 4 API services  
✅ **Centralized log management** với Elasticsearch  
✅ **Beautiful dashboards** với Kibana  
✅ **Advanced log analysis** và search  
✅ **Performance monitoring** qua logs  
✅ **Error tracking** và debugging  

Dashboard sẽ hiển thị logs thực từ các API services, giúp bạn monitor hiệu suất và phát hiện vấn đề kịp thời.

---

**🎉 Chúc mừng! Bạn đã setup thành công ELK Stack logging system!**
