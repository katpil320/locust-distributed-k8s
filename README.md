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

```bash
# Install the chart
helm install my-locust-test https://github.com/katpil320/locust-distributed-helm/releases/download/v0.2.0/locust-distributed-0.2.0.tgz

# Or from source
git clone https://github.com/katpil320/locust-distributed-helm.git
cd locust-distributed-helm && helm install my-locust-test .
```

**Configure storage** (important for persistence):

```yaml
# values.yaml
storage:
  storageClass: "aws-efs" # or azure-file, nfs-client, etc.
```

**Upload test scripts:**

```bash
kubectl port-forward service/my-locust-test-filebrowser 8080:8080
# Visit http://localhost:8080 (admin/admin) and upload locustfile.py
```

**Start testing:**

```bash
kubectl scale deployment my-locust-test-master --replicas=1
kubectl scale deployment my-locust-test-worker --replicas=3
kubectl port-forward service/my-locust-test-master 8089:8089
# Visit http://localhost:8089 to configure and start your load test
```

## ⚙️ Configuration

**Storage Classes** (ReadWriteMany required):

- AWS: `aws-efs` | Azure: `azure-file` | GCP: `filestore-csi` | On-premises: `nfs-client`

**Key Options:**

```yaml
locust:
  targetHost: "https://your-app.com"
  worker:
    replicas: 5
storage:
  storageClass: "aws-efs"
  size: "5Gi"
ingress:
  enabled: true
  locust:
    host: "locust.your-domain.com"
```

## 📁 Examples

Check [`examples/`](./examples/) for:

- **Simple Web Test**: Basic HTTP endpoint testing
- **Advanced Load Test**: Complex scenarios with custom load shapes
- **Data-driven Tests**: Using external JSON data files

## 🔧 Common Commands

```bash
# Check status
kubectl get pods -l app.kubernetes.io/instance=my-locust-test

# Scale workers
kubectl scale deployment my-locust-test-worker --replicas=5

# View logs
kubectl logs deployment/my-locust-test-master
kubectl logs deployment/my-locust-test-worker

# Access UIs
kubectl port-forward service/my-locust-test-filebrowser 8080:8080  # File browser
kubectl port-forward service/my-locust-test-master 8089:8089      # Locust UI
```

## 🚨 Troubleshooting

**Pod stuck in Pending**: `kubectl describe pod <pod-name>` - Check storage class/resources  
**Locust can't find script**: Ensure `locustfile.py` is in root directory via File Browser  
**Workers not connecting**: `kubectl logs deployment/my-locust-test-worker` - Check master service  
**Storage issues**: Verify ReadWriteMany storage class and CSI drivers
