import sys
import yaml
import random
import string
import os
import copy

# The attacker extends the victim pod’s affinity condition by appending 
# additional values from the labels of pods likely to be co-located with the victim.
# (→ Fill in with the victim pod and the labels of pods likely to be co-located with it)
pod_affinity_data = {
    "app": [...],
    "environment": [...],
    "version": [...],
    "component": [...],
    "instance": [...],
    "part-of": [...],
    ...
}

# number of attack pods to generate
DEFAULT_COUNT = 10


def generate_instance_value():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def add_random_values_to_matchexpr(expr):
    key = expr.get("key")
    values = expr.setdefault("values", [])
    existing = set(values)

    if key == "instance":
        new_vals = []
        while len(new_vals) < 2:
            v = generate_instance_value()
            if v not in existing and v not in new_vals:
                new_vals.append(v)
        values.extend(new_vals)
        return

    candidates = pod_affinity_data.get(key, [])
    if not candidates:
        return

    available = [c for c in candidates if c not in existing]
    if not available:
        return

    k = min(2, len(available))
    chosen = random.sample(available, k=k)
    values.extend(chosen)

def mutate_pod_base(base_pod, index):
    pod = copy.deepcopy(base_pod)

    # name definition
    meta = pod.setdefault("metadata", {})
    meta["name"] = f"attacker-{index}"
    labels = meta.setdefault("labels", {})

    # add attacker label(spreading label)
    labels["spread"] = "label"

    # extract podAffinity labelSelector
    spec = pod.setdefault("spec", {})
    affinity = spec.setdefault("affinity", {})
    pod_affinity = affinity.get("podAffinity", {})
    pref = pod_affinity.get("preferredDuringSchedulingIgnoredDuringExecution", [])

    for term in pref:
        label_selector = term.get("podAffinityTerm", {}).get("labelSelector", {})
        match_expressions = label_selector.get("matchExpressions", [])
        for expr in match_expressions:
            add_random_values_to_matchexpr(expr)

    # apply spreading label; add podAntiAffinity
    affinity["podAntiAffinity"] = {
        "requiredDuringSchedulingIgnoredDuringExecution": [
            {
                "labelSelector": {
                    "matchExpressions": [
                        {"key": "spread", "operator": "In", "values": ["label"]}
                    ]
                },
                "topologyKey": "kubernetes.io/hostname"
            }
        ]
    }
    spec["affinity"] = affinity

    # replace containers config
    spec["containers"] = [
        {"image": "nginx:latest", "imagePullPolicy": "IfNotPresent", "name": "attack-container"}
    ]

    return pod

# --- main ---
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script_multi_attackers.py <input_pod_yaml> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        base = yaml.safe_load(f)

    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    created_files = []
    for i in range(1, DEFAULT_COUNT + 1):
        pod_yaml = mutate_pod_base(base, i)
        out_path = os.path.join(out_dir, f"attacker-{i}.yaml")
        with open(out_path, "w") as fo:
            yaml.safe_dump(pod_yaml, fo, sort_keys=False, default_flow_style=False)
        created_files.append(out_path)

    print(f"Created {len(created_files)} files in '{out_dir}':")
    for p in created_files:
        print("  -", p)

if __name__ == "__main__":
    main()
