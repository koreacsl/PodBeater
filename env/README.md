# Kubernetes Cluster Environment Setup

This document explains how to set up the environment for experiments, including:

1. Setting up a **local registry** using Podman
2. Saving Docker images to the local registry
3. Labeling Kubernetes cluster nodes
4. Generating Pod YAML files
5. Deploying generated benign pods into the cluster

---

## 1. Set up a Local Registry

Run a local registry using Podman:

```bash
podman run -d -p 5000:5000 --name local-registry --restart=always registry:2
```

Or with a mounted volume:

```bash
podman run -d \
  --name local-registry \
  -p 5000:5000 \
  -v /var/lib/local-registry \
  --restart=always \
  registry:2
```

Check the running status:

```bash
podman ps
```

---

### Configure containerd to Use the Registry

Edit the containerd configuration:

```bash
sudo vi /etc/containerd/config.toml
```

Add or update:

```toml
[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"
```

Create a certificate directory:

```bash
sudo mkdir -p /etc/containerd/certs.d/<LOCAL_REGISTRY>:5000
```

Create `/etc/containerd/certs.d/<LOCAL_REGISTRY>:5000/hosts.toml`:

```toml
server = "http://<LOCAL_REGISTRY>:5000"

[host."<LOCAL_REGISTRY>:5000"]
  capabilities = ["pull", "resolve"]
  skip_verify = true
```

Restart containerd:

```bash
sudo systemctl restart containerd
```

---

## 2. Save Docker Images into the Local Registry

After the local registry is ready, run the script:

```bash
./local_registry.sh
```

This script pushes the required Docker images into your local registry.

---

## 3. Label Kubernetes Cluster Nodes

Run the following script to add labels to nodes in the Kubernetes cluster:

```bash
./node_label.sh
```

---

## 4. Generate Pod YAML Files

Use the Python script to generate Pod YAML manifests:

```bash
python3 pod_yaml.py
```

This will generate YAML files for benign pods.

---

## 5. Deploy Benign Pods

Apply the generated pod YAML files to your Kubernetes cluster:

```bash
kubectl apply -f <benign pod yaml file or files directory>
```

---

## ⚠️ Notes

* The local registry setup must be applied **on all nodes in the Kubernetes cluster**.
* Replace `<LOCAL_REGISTRY>` with the IP or hostname of your local registry server.
* For secure environments, distribute and use proper certificates instead of `skip_verify = true`.
