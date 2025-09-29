# Kubernetes Deployment Guide

## 📋 Tổng quan

Hướng dẫn chi tiết triển khai dự án 4 Microservices APIs với MongoDB lên Kubernetes cluster. Mỗi service sẽ chạy trong 1 pod riêng biệt với cấu hình tối ưu cho production.

## 🏗️ Kiến trúc Kubernetes

```
┌─────────────────────────────────────────────────────────────────┐
│                        Kubernetes Cluster                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │ User API    │  │Product API  │  │ Order API   │  │Payment API  │  │
│  │ Pod         │  │ Pod         │  │ Pod         │  │ Pod         │  │
│  │ Port: 8000  │  │ Port: 8001  │  │ Port: 8002  │  │ Port: 8003  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
│         │                 │                 │                 │       │
│         └─────────────────┼─────────────────┼─────────────────┘       │
│                           │                 │                         │
│                  ┌─────────────────────────────────────┐               │
│                  │           MongoDB Pod               │               │
│                  │         Port: 27017                 │               │
│                  └─────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Chuẩn bị triển khai

### 1. Yêu cầu hệ thống

#### Kubernetes Cluster
- **Minikube**: Cho development
- **Docker Desktop**: Với Kubernetes enabled
- **Cloud**: GKE, EKS, AKS
- **On-premise**: kubeadm, k3s

#### Tools cần thiết
```bash
# Kiểm tra kubectl
kubectl version --client

# Kiểm tra cluster
kubectl cluster-info

# Kiểm tra nodes
kubectl get nodes
```

### 2. Build Docker Images

Trước khi deploy, cần build Docker images cho các APIs:

```bash
# Build images từ source code
docker build -t user-api:latest ./api1
docker build -t product-api:latest ./api2
docker build -t order-api:latest ./api3
docker build -t payment-api:latest ./api4

# Tag images cho registry (nếu cần)
docker tag user-api:latest your-registry.com/user-api:v1.0.0
docker tag product-api:latest your-registry.com/product-api:v1.0.0
docker tag order-api:latest your-registry.com/order-api:v1.0.0
docker tag payment-api:latest your-registry.com/payment-api:v1.0.0

# Push to registry
docker push your-registry.com/user-api:v1.0.0
docker push your-registry.com/product-api:v1.0.0
docker push your-registry.com/order-api:v1.0.0
docker push your-registry.com/payment-api:v1.0.0
```

## 📦 Triển khai Services

### 1. MongoDB Deployment

```bash
# Deploy MongoDB trước
kubectl apply -f k8s/mongodb-deployment.yaml

# Kiểm tra MongoDB pod
kubectl get pods -l app=mongodb
kubectl logs deployment/mongodb

# Test MongoDB connection
kubectl exec -it deployment/mongodb -- mongosh --eval "db.adminCommand('ping')"
```

**Cấu hình MongoDB:**
- **Image**: mongo:7.0
- **Storage**: emptyDir (temporary)
- **Resources**: 512Mi-1Gi RAM, 250m-500m CPU
- **Health Checks**: Liveness và Readiness probes

### 2. APIs Deployment

```bash
# Deploy tất cả APIs
kubectl apply -f k8s/user-api-deployment.yaml
kubectl apply -f k8s/product-api-deployment.yaml
kubectl apply -f k8s/order-api-deployment.yaml
kubectl apply -f k8s/payment-api-deployment.yaml

# Hoặc sử dụng script
chmod +x k8s/deploy.sh
./k8s/deploy.sh
```

### 3. Kiểm tra Deployment

```bash
# Xem tất cả resources
kubectl get all

# Xem pods status
kubectl get pods

# Xem services
kubectl get services

# Xem logs
kubectl logs deployment/user-api
kubectl logs deployment/product-api
kubectl logs deployment/order-api
kubectl logs deployment/payment-api
```

## 🌐 Truy cập Services

### 1. LoadBalancer Services

Các API services sử dụng LoadBalancer type:

```bash
# Lấy external IPs
kubectl get services

# Output example:
# NAME                TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)
# user-api-service    LoadBalancer   10.96.1.2       192.168.1.100   8000:30001/TCP
# product-api-service LoadBalancer   10.96.1.3       192.168.1.101   8001:30002/TCP
# order-api-service   LoadBalancer   10.96.1.4       192.168.1.102   8002:30003/TCP
# payment-api-service LoadBalancer   10.96.1.5       192.168.1.103   8003:30004/TCP
```

### 2. Test APIs

```bash
# Test User API
curl http://192.168.1.100:8000/health

# Test Product API
curl http://192.168.1.101:8001/health

# Test Order API
curl http://192.168.1.102:8002/health

# Test Payment API
curl http://192.168.1.103:8003/health
```

### 3. Port Forwarding (Alternative)

Nếu không có LoadBalancer, sử dụng port forwarding:

```bash
# Port forward cho local access
kubectl port-forward service/user-api-service 8000:8000 &
kubectl port-forward service/product-api-service 8001:8001 &
kubectl port-forward service/order-api-service 8002:8002 &
kubectl port-forward service/payment-api-service 8003:8003 &
kubectl port-forward service/mongodb-service 27017:27017 &

# Test local
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

## 🔧 Cấu hình chi tiết

### 1. Resource Management

#### MongoDB Resources
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

#### API Resources
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "250m"
```

### 2. Health Checks

#### Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

#### Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 3. Environment Variables

```yaml
env:
- name: DJANGO_SETTINGS_MODULE
  value: "userapi.settings"
- name: MONGODB_HOST
  value: "mongodb-service"
- name: MONGODB_PORT
  value: "27017"
```

## 📊 Monitoring và Debugging

### 1. Pod Status

```bash
# Xem pod status
kubectl get pods -o wide

# Xem pod details
kubectl describe pod <pod-name>

# Xem pod logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Previous container logs
```

### 2. Service Status

```bash
# Xem service details
kubectl describe service <service-name>

# Test service connectivity
kubectl exec -it <pod-name> -- curl localhost:8000/health
```

### 3. Events và Troubleshooting

```bash
# Xem events
kubectl get events --sort-by=.metadata.creationTimestamp

# Xem resource usage
kubectl top pods
kubectl top nodes

# Debug pod issues
kubectl exec -it <pod-name> -- /bin/bash
```

## 🐛 Xử lý lỗi thường gặp

### 1. Pod không start

**Lỗi**: `Pod is in Pending state`

**Nguyên nhân**: Không đủ resources hoặc image không tồn tại

**Giải pháp**:
```bash
# Kiểm tra events
kubectl describe pod <pod-name>

# Kiểm tra resources
kubectl top nodes

# Kiểm tra image
kubectl get pod <pod-name> -o yaml | grep image
```

### 2. Service không accessible

**Lỗi**: `Connection refused`

**Nguyên nhân**: Service selector không match với pod labels

**Giải pháp**:
```bash
# Kiểm tra service selector
kubectl get service <service-name> -o yaml

# Kiểm tra pod labels
kubectl get pods --show-labels

# Test connectivity
kubectl exec -it <pod-name> -- curl localhost:8000
```

### 3. MongoDB connection failed

**Lỗi**: `MongoDB connection timeout`

**Nguyên nhân**: MongoDB chưa ready hoặc network issue

**Giải pháp**:
```bash
# Kiểm tra MongoDB pod
kubectl logs deployment/mongodb

# Test MongoDB connection
kubectl exec -it deployment/mongodb -- mongosh --eval "db.adminCommand('ping')"

# Kiểm tra service
kubectl get service mongodb-service
```

### 4. Image pull errors

**Lỗi**: `ImagePullBackOff`

**Nguyên nhân**: Image không tồn tại hoặc registry không accessible

**Giải pháp**:
```bash
# Kiểm tra image
docker images | grep user-api

# Build lại image
docker build -t user-api:latest ./api1

# Hoặc sử dụng image từ registry
kubectl set image deployment/user-api user-api=your-registry.com/user-api:v1.0.0
```

## 🔄 Scaling và Updates

### 1. Scale APIs

```bash
# Scale User API
kubectl scale deployment user-api --replicas=3

# Scale tất cả APIs
kubectl scale deployment user-api product-api order-api payment-api --replicas=3

# Kiểm tra scaling
kubectl get deployments
kubectl get pods -l app=user-api
```

### 2. Rolling Updates

```bash
# Update image
kubectl set image deployment/user-api user-api=user-api:v2.0.0

# Kiểm tra rollout status
kubectl rollout status deployment/user-api

# Rollback nếu cần
kubectl rollout undo deployment/user-api
```

### 3. Auto Scaling

```bash
# Tạo HPA cho User API
kubectl autoscale deployment user-api --cpu-percent=50 --min=1 --max=10

# Xem HPA status
kubectl get hpa
```

## 🛡️ Security và Best Practices

### 1. Secrets Management

```yaml
# Tạo secret cho MongoDB
apiVersion: v1
kind: Secret
metadata:
  name: mongodb-secret
type: Opaque
data:
  username: YWRtaW4=  # admin
  password: cGFzc3dvcmQxMjM=  # password123
```

### 2. Network Policies

```yaml
# Network policy cho APIs
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: user-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 8000
```

### 3. Resource Quotas

```yaml
# Resource quota cho namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: api-quota
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 4Gi
    limits.cpu: "4"
    limits.memory: 8Gi
```

## 📈 Production Deployment

### 1. Persistent Storage

```yaml
# PersistentVolume cho MongoDB
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

### 2. Ingress Controller

```yaml
# Ingress cho APIs
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: user-api-service
            port:
              number: 8000
      - path: /products
        pathType: Prefix
        backend:
          service:
            name: product-api-service
            port:
              number: 8001
```

### 3. Monitoring Setup

```yaml
# ServiceMonitor cho Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-monitor
spec:
  selector:
    matchLabels:
      app: user-api
  endpoints:
  - port: 8000
    path: /metrics
```

## 🧹 Cleanup

### 1. Cleanup Script

```bash
# Chạy cleanup script
chmod +x k8s/cleanup.sh
./k8s/cleanup.sh
```

### 2. Manual Cleanup

```bash
# Xóa deployments
kubectl delete -f k8s/mongodb-deployment.yaml
kubectl delete -f k8s/user-api-deployment.yaml
kubectl delete -f k8s/product-api-deployment.yaml
kubectl delete -f k8s/order-api-deployment.yaml
kubectl delete -f k8s/payment-api-deployment.yaml

# Xóa tất cả resources
kubectl delete all --all
```

## 📚 Useful Commands

### 1. Basic Commands

```bash
# Xem tất cả resources
kubectl get all

# Xem pods với labels
kubectl get pods --show-labels

# Xem services với endpoints
kubectl get endpoints

# Xem events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### 2. Debug Commands

```bash
# Xem pod logs
kubectl logs <pod-name> -f

# Vào pod
kubectl exec -it <pod-name> -- /bin/bash

# Xem pod details
kubectl describe pod <pod-name>

# Xem service details
kubectl describe service <service-name>
```

### 3. Management Commands

```bash
# Restart deployment
kubectl rollout restart deployment/user-api

# Scale deployment
kubectl scale deployment/user-api --replicas=3

# Update image
kubectl set image deployment/user-api user-api=user-api:v2.0.0

# Rollback
kubectl rollout undo deployment/user-api
```

## 🎯 Kết luận

Với cấu hình này, bạn có thể triển khai thành công dự án 4 Microservices APIs lên Kubernetes với:

- ✅ **High Availability**: Mỗi service chạy trong pod riêng biệt
- ✅ **Scalability**: Có thể scale từng service độc lập
- ✅ **Health Monitoring**: Liveness và Readiness probes
- ✅ **Resource Management**: CPU và Memory limits
- ✅ **Service Discovery**: Kubernetes DNS cho internal communication
- ✅ **Load Balancing**: LoadBalancer services cho external access

Dự án đã sẵn sàng cho production deployment với các cấu hình bảo mật và monitoring phù hợp.
