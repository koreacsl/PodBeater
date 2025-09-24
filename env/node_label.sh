#!/bin/bash

# ================================================
# Node Labeling Script for Kubernetes Cluster
#
# - Modify the label values (memory, cpu-type, gpu-type, storage-type, etc.)
#   according to the actual specifications of your cluster nodes.
# - Each key in 'node_labels' should match the node name in your cluster.
# - Run this script to apply or overwrite labels for all nodes.
# ================================================


declare -A node_labels

node_labels["k8s-worker1"]="memory=6 cpu-type=mips64 gpu-type=nvidia-tesla storage-type=sshd"
node_labels["k8s-worker2"]="memory=4 cpu-type=mips32 gpu-type=amd-rdnd storage-type=sata"
node_labels["k8s-worker3"]="memory=5 cpu-type=ppc32 gpu-type=nvidia-hopper storage-type=hdd"
node_labels["k8s-worker4"]="memory=3 cpu-type=arm64 gpu-type=amd-radeon storage-type=hdd"
node_labels["k8s-worker5"]="memory=4 cpu-type=mips32 gpu-type=amd-radeon storage-type=sata"
node_labels["k8s-worker6"]="memory=3 cpu-type=ppc64 gpu-type=nvidia-hopper storage-type=hdd"
node_labels["k8s-worker7"]="memory=5 cpu-type=arm32 gpu-type=amd-rdnd storage-type=hdd"
node_labels["k8s-worker8"]="memory=4 cpu-type=ppc32 gpu-type=amd-rdnd storage-type=ssd"
node_labels["k8s-worker9"]="memory=5 cpu-type=ppc64 gpu-type=amd-radeon storage-type=hdd"
node_labels["k8s-worker10"]="memory=4 cpu-type=arm32 gpu-type=nvidia-tesla storage-type=sshd"
node_labels["k8s-worker11"]="memory=5 cpu-type=mips32 gpu-type=nvidia-rtx storage-type=hdd"
node_labels["k8s-worker12"]="memory=3 cpu-type=ppc64 gpu-type=nvidia-tesla storage-type=sshd"
node_labels["k8s-worker13"]="memory=4 cpu-type=mips64 gpu-type=nvidia-tesla storage-type=sshd"
node_labels["k8s-worker14"]="memory=6 cpu-type=amd64 gpu-type=amd-radeon storage-type=nvme"
node_labels["k8s-worker15"]="memory=4 cpu-type=arm32 gpu-type=amd-radeon storage-type=sata"
node_labels["k8s-worker16"]="memory=3 cpu-type=arm64 gpu-type=amd-rdnd storage-type=ssd"
node_labels["k8s-worker17"]="memory=4 cpu-type=mips64 gpu-type=nvidia-tesla storage-type=nvme"
node_labels["k8s-worker18"]="memory=5 cpu-type=amd64 gpu-type=amd-rdnd storage-type=hdd"
node_labels["k8s-worker19"]="memory=3 cpu-type=arm32 gpu-type=nvidia-hopper storage-type=sshd"
node_labels["k8s-worker20"]="memory=4 cpu-type=mips32 gpu-type=nvidia-tesla storage-type=sata"
node_labels["k8s-worker21"]="memory=3 cpu-type=ppc64 gpu-type=amd-rdnd storage-type=hdd"
node_labels["k8s-worker22"]="memory=5 cpu-type=arm32 gpu-type=amd-rdnd storage-type=sata"
node_labels["k8s-worker23"]="memory=3 cpu-type=ppc32 gpu-type=nvidia-tesla storage-type=nvme"
node_labels["k8s-worker24"]="memory=6 cpu-type=ppc64 gpu-type=amd-radeon storage-type=sata"
node_labels["k8s-worker25"]="memory=4 cpu-type=ppc64 gpu-type=nvidia-rtx storage-type=sshd"
node_labels["k8s-worker26"]="memory=6 cpu-type=mips32 gpu-type=nvidia-hopper storage-type=hdd"
node_labels["k8s-worker27"]="memory=3 cpu-type=mips32 gpu-type=amd-rdnd storage-type=hdd"
node_labels["k8s-worker28"]="memory=5 cpu-type=ppc64 gpu-type=amd-rdnd storage-type=nvme"
node_labels["k8s-worker29"]="memory=3 cpu-type=amd64 gpu-type=nvidia-hopper storage-type=ssd"
node_labels["k8s-worker30"]="memory=6 cpu-type=amd64 gpu-type=amd-radeon storage-type=hdd"
node_labels["k8s-worker31"]="memory=5 cpu-type=mips32 gpu-type=nvidia-hopper storage-type=ssd"
node_labels["k8s-worker32"]="memory=3 cpu-type=arm64 gpu-type=nvidia-hopper storage-type=nvme"
node_labels["k8s-worker33"]="memory=5 cpu-type=mips32 gpu-type=amd-radeon storage-type=sata"
node_labels["k8s-worker34"]="memory=6 cpu-type=arm32 gpu-type=nvidia-hopper storage-type=sata"
node_labels["k8s-worker35"]="memory=4 cpu-type=mips64 gpu-type=nvidia-rtx storage-type=sshd"
node_labels["k8s-worker36"]="memory=6 cpu-type=ppc32 gpu-type=amd-rdnd storage-type=hdd"
node_labels["k8s-worker37"]="memory=3 cpu-type=ppc64 gpu-type=amd-rdnd storage-type=ssd"
node_labels["k8s-worker38"]="memory=6 cpu-type=arm32 gpu-type=amd-rdnd storage-type=nvme"
node_labels["k8s-worker39"]="memory=3 cpu-type=mips32 gpu-type=amd-rdnd storage-type=sshd"
node_labels["k8s-worker40"]="memory=4 cpu-type=amd64 gpu-type=amd-radeon storage-type=nvme"

# apply labels to each node
for node in "${!node_labels[@]}"; do
    echo "Labeling $node with ${node_labels[$node]}"
    kubectl label nodes "$node" ${node_labels[$node]} --overwrite
done
