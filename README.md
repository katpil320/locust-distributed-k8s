# Locust Distributed Load Testing Helm Chart

A Helm chart for deploying distributed [Locust](https://locust.io/) load testing environment on Kubernetes with file browser integration for easy script management.

## ✨ Features

- **🚀 Distributed Locust Setup**: Scalable master-worker architecture
- **📁 File Browser Integration**: Web-based file management for test scripts and data
- **💾 Shared Storage**: Persistent volume shared between all pods
- **🔧 Configurable**: Highly customizable via Helm values
- **📊 Production Ready**: Resource limits, security contexts, and best practices
- **🎯 Generic Design**: Works with any Locust test scripts

## 📋 Prerequisites

- Kubernetes cluster (1.19+)
- Helm 3.0+
- Storage class that supports `ReadWriteMany` access mode (e.g., EFS, NFS, Azure Files)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File Browser  │    │  Locust Master  │    │ Locust Workers  │
│                 │    │                 │    │                 │
│  - Upload files │    │  - Web UI       │    │  - Execute tests│
│  - Manage data  │    │  - Coordinate   │    │  - Auto-scale   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │    Shared Storage       │
                    │   /mnt/locust           │
                    │                         │
                    │ - locustfile.py         │
                    │ - test data             │
                    │ - results & logs        │
                    └─────────────────────────┘
```

## 🚀 Quick Start

### 1. Install the Chart

```bash
# Clone the repository
git clone https://github.com/katpil320/locust-distributed-helm.git
cd locust-distributed-helm

# Install with Helm
helm install my-locust-test .
```

### 2. Configure Storage (Important!)

Update `values.yaml` with your storage class:

```yaml
storage:
  storageClass: "your-rwx-storage-class" # e.g., "aws-efs", "azure-file", "nfs-client"
```

### 3. Upload Your Test Scripts

```bash
# Port forward to file browser
kubectl port-forward service/my-locust-test-filebrowser 8080:8080

# Access file browser at http://localhost:8080
# Default credentials: admin / admin
# Upload your locustfile.py to the root directory
```

### 4. Start Load Testing

```bash
# Scale up the master
kubectl scale deployment my-locust-test-master --replicas=1

# Scale up workers (adjust number as needed)
kubectl scale deployment my-locust-test-worker --replicas=3

# Access Locust Web UI
kubectl port-forward service/my-locust-test-master 8089:8089
# Open http://localhost:8089
```

## 📖 Detailed Installation Guide

### Using Helm Repository (Recommended)

```bash
# Add the Helm repository
helm repo add locust-distributed https://katpil320.github.io/locust-distributed-helm
helm repo update

# Install the chart
helm install my-locust-test locust-distributed/locust-distributed
```

### From Source

```bash
# Clone and install locally
git clone https://github.com/katpil320/locust-distributed-helm.git
cd locust-distributed-helm
helm install my-locust-test .
```

### With Custom Configuration

```bash
# Create custom values file
cat > my-values.yaml << EOF
storage:
  storageClass: "aws-efs"
  size: "5Gi"

locust:
  master:
    replicas: 1
  worker:
    replicas: 5
    resources:
      limits:
        cpu: 500m
        memory: 1Gi

ingress:
  enabled: true
  locust:
    host: "locust.example.com"
  filebrowser:
    host: "files.example.com"
EOF

# Install with custom values
helm install my-locust-test . -f my-values.yaml
```

## 📚 Usage Workflow

### 1. Install and Setup

```bash
helm install my-locust-test .
```

> **Note**: All Locust pods start with 0 replicas. You'll scale them after uploading your test scripts.

### 2. Prepare Your Test Scripts

- Use the examples in the `examples/` directory as starting points
- See [Examples Documentation](./examples/README.md) for detailed guides
- Ensure your main script is named `locustfile.py`

### 3. Upload Scripts via File Browser

```bash
# Port forward to file browser
kubectl port-forward service/my-locust-test-filebrowser 8080:8080
```

- Open http://localhost:8080 in your browser
- Login with default credentials: `admin` / `admin`
- Upload your `locustfile.py` to the root directory
- Upload any additional test data files

### 4. Scale Up and Start Testing

```bash
# Scale up the master (always 1 replica)
kubectl scale deployment my-locust-test-master --replicas=1

# Scale up workers (adjust based on your needs)
kubectl scale deployment my-locust-test-worker --replicas=3

# Access Locust Web UI
kubectl port-forward service/my-locust-test-master 8089:8089
```

- Open http://localhost:8089
- Configure target host, number of users, and spawn rate
- Start your load test!

### 5. Monitor and Analyze

- Watch real-time metrics in the Locust Web UI
- Download test results and reports
- Monitor Kubernetes resources: `kubectl top pods`

### 6. Scale Down After Testing

```bash
# Scale down when finished
kubectl scale deployment my-locust-test-master --replicas=0
kubectl scale deployment my-locust-test-worker --replicas=0
```

## ⚙️ Configuration

### Storage Classes

This chart requires a storage class that supports `ReadWriteMany` access mode:

| Cloud Provider | Storage Class   | Notes                         |
| -------------- | --------------- | ----------------------------- |
| AWS            | `aws-efs`       | Requires EFS CSI driver       |
| Azure          | `azure-file`    | Built-in Azure Files          |
| GCP            | `filestore-csi` | Requires Filestore CSI driver |
| On-premises    | `nfs-client`    | Requires NFS provisioner      |

### Resource Requirements

| Component    | Default CPU | Default Memory | Scaling Notes       |
| ------------ | ----------- | -------------- | ------------------- |
| Master       | 100m-500m   | 128Mi-512Mi    | Single replica only |
| Worker       | 100m-200m   | 128Mi-256Mi    | Scale horizontally  |
| File Browser | 50m-100m    | 64Mi-128Mi     | Single replica only |

### Key Configuration Options

```yaml
# Target application (can be changed in Web UI)
locust:
  targetHost: "https://your-app.com"

  # Worker scaling
  worker:
    replicas: 5 # Adjust based on load requirements

# Storage configuration
storage:
  storageClass: "your-rwx-storage-class"
  size: "5Gi"

# Enable ingress for external access
ingress:
  enabled: true
  locust:
    host: "locust.your-domain.com"
  filebrowser:
    host: "files.your-domain.com"
```

## 📁 Example Test Scripts

Check out the `examples/` directory for:

- **Simple Web Test**: Basic HTTP endpoint testing
- **Advanced Load Test**: Complex user journeys with custom load shapes
- **Data-driven Tests**: Using external JSON data files

See [Examples README](./examples/README.md) for detailed documentation.

## 🔧 Advanced Usage

### Custom Load Shapes

Use custom load shapes for realistic traffic patterns:

```python
from locust import LoadTestShape

class MyLoadShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()
        if run_time < 300:  # 5 minutes ramp-up
            return (run_time // 10, 2)  # Gradual increase
        return (50, 2)  # Steady state
```

### Horizontal Pod Autoscaling

Enable HPA for automatic worker scaling:

```bash
kubectl autoscale deployment my-locust-test-worker --cpu-percent=70 --min=2 --max=20
```

### Multiple Test Environments

Deploy multiple instances for different environments:

```bash
# Production testing
helm install prod-load-test . -f prod-values.yaml

# Staging testing
helm install staging-load-test . -f staging-values.yaml
```

## 🚨 Troubleshooting

### Common Issues

**Pod stuck in Pending state**

```bash
kubectl describe pod <pod-name>
# Check for storage class issues or resource constraints
```

**Locust can't find locustfile.py**

- Ensure file is uploaded to root directory in File Browser
- Check file permissions and naming (must be exactly `locustfile.py`)

**Workers not connecting to master**

```bash
# Check worker logs
kubectl logs deployment/my-locust-test-worker

# Verify master service
kubectl get svc my-locust-test-master
```

**Storage mount issues**

- Verify your storage class supports ReadWriteMany
- Check if CSI drivers are installed for your storage type

### Getting Help

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/name=locust-distributed

# View logs
kubectl logs -l app.kubernetes.io/component=master
kubectl logs -l app.kubernetes.io/component=worker

# Describe resources
kubectl describe deployment my-locust-test-master
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development

```bash
# Clone and setup
git clone https://github.com/katpil320/locust-distributed-helm.git
cd locust-distributed-helm

# Test locally
helm template . | kubectl apply --dry-run=client -f -

# Package for release
helm package .
```

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Locust](https://locust.io/) - The amazing load testing framework
- [File Browser](https://filebrowser.org/) - Web-based file management
- Kubernetes and Helm communities

---

## Example Locust Script

For quick testing, here's a minimal example:

```python
from locust import HttpUser, task, between

class QuickTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_homepage(self):
        self.client.get("/")

    @task
    def test_api(self):
        self.client.get("/api/health")
```

📖 **For more examples and detailed guides, see [examples/README.md](./examples/README.md)**

Save this as `locustfile.py` and upload via File Browser:

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_homepage(self):
        self.client.get("/")

    @task(1)
    def view_api(self):
        self.client.get("/api/health")

    def on_start(self):
        # Login or setup code
        pass
```

## Troubleshooting

### Common Issues

1. **Workers not connecting to master / script not working**:

   ```bash
   # Check master service
   kubectl get svc locust-distributed-master

   # Check worker logs
   kubectl logs -l app.kubernetes.io/component=worker
   ```

2. **File not found errors**:

   ```bash
   # Verify file upload
   kubectl exec -it deployment/locust-distributed-filebrowser -- ls -la /srv

   # Check volume mounts
   kubectl describe pod -l app.kubernetes.io/component=master
   ```

3. **Storage issues**:

   ```bash
   # Check PVC status
   kubectl get pvc

   # Describe PVC for events
   kubectl describe pvc locust-distributed-storage
   ```

## Cleanup

```bash
# Uninstall the release
helm uninstall locust-distributed
```
