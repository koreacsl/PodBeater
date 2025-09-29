# PodBeater Attack Cost Evaluation

This document outlines the procedure for measuring the **attack cost** against various threat models using the **PodBeater** attack in a **Kubernetes cluster**.

## 1. Kubernetes Cluster Setup
The tests will be conducted on two different cluster sizes. All nodes will use **containerd** as their container runtime.

- **Small-scale Cluster**: 1 master node, 20 worker nodes
- **Large-scale Cluster**: 1 master node, 40 worker nodes

-----

## 2. Environment Configuration
You'll need to set up the environment as described in the `/env` folder.

The following description outlines only the basic steps; for detailed setup instructions, please refer to the `README.md` file in the `/env` folder.

### 2.1. Local Registry Setup
To provide the required images for deploying attack and benign pods, set up a local registry within the cluster.

```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
````

### 2.2. Node Labeling

Label each node with a specific node label.

```bash
./node_label
```

### 2.3. Benign Pod Deployment

Deploy benign pods that will serve as targets. Deploy multiple pods so you can select a specific one or a random one to attack.

```bash
kubectl apply -f <benign pods directory>
```

-----

## 3. Generating and Deploying Attack Pods by Threat Model

Run the script to create attack pods according to two threat models: **Tu** and **Tr**.

### 3.1. Threat Model Tu

In this scenario, the attacker does have knowledge of the victim pod’s scheduling requirements.

  - **`PodBeater_same`**: Extends the victim’s scheduling requirements with additional values.
  - **`PodBeater_random`**: Extends the victim’s scheduling requirements with new values each attempt.

    
<!-- end list -->

```bash
# Generate PodBeater_same attack pods
python3 PodBeater_same.py <path/to/target_pod_yaml> <path/to/attack_pod_yaml>

# Generate PodBeater_random attack pods
python3 PodBeater_random.py <path/to/target_pod_yaml> <path/to/attack_pods_directory>
```

### 3.2. Threat Model Tr

In this scenario, the attacker has no knowledge of the victim pod’s requirements.

  - **`PodBeater_v3`**: Scheduling requirements configured as 3 multi-value.
  - **`PodBeater_v5`**: Scheduling requirements configured as 5 multi-value.

<!-- end list -->

```bash
# PodBeater_v3 behavior
python3 PodBeater_Tr.py --multi-value 3 --out-dir attack_pods_v3

# PodBeater_v5 behavior 
python3 PodBeater_Tr.py --multi-value 5 --out-dir attack_pods_v5
```

-----

## 4. Measuring Attack Cost

### 4.1. Target Selection

Choose one of the deployed benign pods as the **target pod**.

### 4.2. Run the Script

Update the `attack_cost.sh` script with the name of your selected target pod. After making the change, run the script to measure the attack cost.

```bash
# attack_cost.sh
# Declaration section
TARGET_POD="selected-target-pod-name"
ATTACKER_DIR="created-attack-pod-directory"
...

# Run the script
./attack_cost.sh
```
