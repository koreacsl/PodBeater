import random
import yaml
import os
import argparse

# number of pods to generate
NUM_PODS = 20

def generate_pod_yaml(pod_name, extra_values, multi_value_count=3, image="nginx:latest"):

    # Randomly pick 3 distinct label keys
    selected_keys = random.sample(list(extra_values.keys()), 3)

    pod_affinity = {"preferredDuringSchedulingIgnoredDuringExecution": []}
    pod_anti_affinity = {"requiredDuringSchedulingIgnoredDuringExecution": []}

    # generate matchExpressions for podAffinityTerm
    required_match_expressions = []
    for key in selected_keys:
        available_values = list(extra_values.get(key, []))
        if not available_values:
            additional_values = []
        else:
            k = min(multi_value_count, len(available_values))
            additional_values = random.sample(available_values, k)

        required_match_expressions.append({
            "key": key,
            "operator": "In",
            "values": additional_values
        })

    pod_affinity["preferredDuringSchedulingIgnoredDuringExecution"].append({
        "weight": 50,
        "podAffinityTerm": {
            "labelSelector": {"matchExpressions": required_match_expressions},
            "topologyKey": "kubernetes.io/hostname"
        }
    })

    # apply spreading label
    pod_anti_affinity["requiredDuringSchedulingIgnoredDuringExecution"].append({
        "labelSelector": {
            "matchExpressions": [
                {"key": "spread", "operator": "In", "values": ["label"]}
            ]
        },
        "topologyKey": "kubernetes.io/hostname"
    })

    metadata_labels = {
        "spread": "label",
        "instance": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
    }

    pod_yaml = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": pod_name, "labels": metadata_labels},
        "spec": {
            "affinity": {
                "podAffinity": pod_affinity,
                "podAntiAffinity": pod_anti_affinity
            },
            "containers": [
                {"name": "attack-container", "image": image, "imagePullPolicy": "IfNotPresent"}
            ]
        }
    }

    return pod_yaml

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate multi-value attack pod YAMLs for Tr experiments (attacker has no victim info)."
    )
    parser.add_argument("--multi-value", "-m", type=int, choices=[3,5], default=3,
                        help="Number of values to sample per selected label (3 for 3 multi-value, 5 for 5 multi-value). Default: 3")
    parser.add_argument("--out-dir", "-o", type=str, default="3_multiV_attack_pods",
                        help="Output directory for generated pod YAML files (default: 3_multiV_attack_pods)")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    multi_value_count = args.multi_value
    out_dir = args.out_dir

    # label pools for keys and values; define and use it according to the type of Docker service you use and your cluster settings
    extra_values = {
        "app": [...],
        "environment": [...],
        "version": [...],
        "component": [...],
        "instance": [...],
        "part-of": [...],
        ...
    }

    os.makedirs(out_dir, exist_ok=True)

    created_files = []
    for i in range(1, NUM_PODS + 1):
        pod_name = f"attack-pod-{i}"
        pod_yaml = generate_pod_yaml(pod_name, extra_values, multi_value_count=multi_value_count)
        file_path = os.path.join(out_dir, f"{pod_name}.yaml")
        with open(file_path, "w", encoding="utf-8") as fo:
            yaml.safe_dump(pod_yaml, fo, sort_keys=False, default_flow_style=False)
        created_files.append(file_path)

    print(f"{len(created_files)} Pod YAML files generated successfully in '{out_dir}' (multi-value={multi_value_count})")
    for p in created_files:
        print("  -", p)

if __name__ == "__main__":
    main()
