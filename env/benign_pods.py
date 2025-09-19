import random
import os
import yaml
import string

# output directory
output_dir = "benign_pods"
os.makedirs(output_dir, exist_ok=True)

# docker services
services = {
    "traefik": {
        "image_prefix": "traefik",
        "versions": ["3.1", "3.0", "2.11", "2.10", "2.8"],
        "container_name": "traefik",
    },
    "nginx": {
        "image_prefix": "nginx",
        "versions": ["1.26.1", "latest", "1.27.1", "1.26", "1.27.3"],
        "container_name": "nginx",
    },
    "tomcat": {
        "image_prefix": "tomcat",
        "versions": ["11.0.1", "10.1.33", "9.0.97", "9.0.96", "10.1.31"],
        "container_name": "tomcat",
    },
    "redis": {
        "image_prefix": "redis",
        "versions": ["7.4.2", "7.4", "7.2", "6.2", "7.0"],
        "container_name": "redis",
    },
    "mongo": {
        "image_prefix": "mongo",
        "versions": ["8.0", "7.0.15", "8.0.3", "6.0.19", "6.0"],
        "container_name": "mongo",
    },
    "wordpress": {
        "image_prefix": "wordpress",
        "versions": ["php8.3", "php8.2", "php8.1", "apache", "6.7.1-php8.3"],
        "container_name": "wordpress",
    },
    "alpine": {
        "image_prefix": "alpine",
        "versions": ["3.20", "3.19", "3.18", "3.17", "3.16"],
        "container_name": "alpine",
    },
    "busybox": {
        "image_prefix": "busybox",
        "versions": ["1.37", "1.36", "1.35", "1.34", "1.33"],
        "container_name": "busybox",
    },
    "python": {
        "image_prefix": "python",
        "versions": ["3.13.0", "3.13", "3.12.7", "3.12"],
        "container_name": "python",
    },
    "registry": {
        "image_prefix": "registry",
        "versions": ["2.8.3", "2.8", "2.8.2", "2.8.1", "2.7"],
        "container_name": "registry",
    },
    "httpd": {
        "image_prefix": "httpd",
        "versions": ["2.4.62", "2.4", "2.4.61", "2.4.60", "2.4.59"],
        "container_name": "httpd",
    },
    "memcached": {
        "image_prefix": "memcached",
        "versions": ["1.6.32", "1.6", "1.6.30", "1.6.29", "1.6.28"],
        "container_name": "memcached",
    },
    "golang": {
        "image_prefix": "golang",
        "versions": ["1.23.3", "1.23", "1.22.9", "1.22", "1.23.2"],
        "container_name": "golang",
    },
    "node": {
        "image_prefix": "node",
        "versions": ["18.20.5", "20.18.1", "23.3", "23.3.0"],
        "container_name": "node",
    },
    "rabbitmq": {
        "image_prefix": "rabbitmq",
        "versions": ["4.0", "4.0.5", "3.13.7", "3.12.14", "4.0.3"],
        "container_name": "rabbitmq",
    },
    "openjdk": {
        "image_prefix": "openjdk",
        "versions": ["24-oracle", "24", "23-jdk", "23"],
        "container_name": "openjdk",
    },
    "sonarqube": {
        "image_prefix": "sonarqube",
        "versions": ["9.9.7-enterprise", "10.7-enterprise", "10.8-developer", "9.9.7-developer"],
        "container_name": "sonarqube",
    },
    "ruby": {
        "image_prefix": "ruby",
        "versions": ["3.3.6", "3.3", "3.2.6", "3.2", "3.1.6"],
        "container_name": "ruby",
    },
    "maven": {
        "image_prefix": "maven",
        "versions": ["3.9.9", "3.8", "3.9.8", "3.9.6", "3.8.8"],
        "container_name": "maven",
    },
    "caddy": {
        "image_prefix": "caddy",
        "versions": ["builder", "2.9", "2.8.4", "2.8", "2.8.1"],
        "container_name": "caddy",
    },
    "eclipse-mosquitto": {
        "image_prefix": "eclipse-mosquitto",
        "versions": ["2.0.20", "2.0.19", "2.0.18", "2.0.17", "2.0.16"],
        "container_name": "eclipse-mosquitto",
    },
    "vault": {
        "image_prefix": "vault",
        "versions": ["1.12.7", "1.11.11", "1.12.5", "1.13.2", "1.13.3"],
        "container_name": "vault",
    },
    "dart": {
        "image_prefix": "dart",
        "versions": ["3.7.1", "3.7", "3.7.0", "3.6.2", "3.6"],
        "container_name": "dart",
    },
    "matoma": {
        "image_prefix": "matoma",
        "versions": ["5.2.2", "5.2", "5.2.1", "5.1.2", "5.0.3"],
        "container_name": "matoma",
    },
    "telegraf": {
        "image_prefix": "telegraf",
        "versions": ["1.33.3", "1.33", "1.33.2", "1.32", "1.30"],
        "container_name": "telegraf",
    },
}

# pod label common data
pod_affinity_data = {
    "app": [],
    "environment": ["production", "staging", "development", "testing", "qa"],
    "version": [],
    "component": [
        "access-control", "orchestration", "proxy", "caching-system",
        "web-server", "database", "api-gateway", "auth",
        "message-broker", "logger", "edge-router", "storage", "data-center"
    ],
    "instance": [],  # instance value handled by separate logic (random)
    "part-of": [
        "wordpress",
        "ecommerce-platform",
        "monitoring-stack",
        "data-analytics",
        "logging-system",
        "customer-service-app",
        "recommendation-engine",
        "messaging-service",
        "devops-toolchain",
        "ml-pipeline"
  ],
  "managed-by": [
        "Helm",
        "Kustomize",
        "Terraform",
        "Ansible",
        "FluxCD",
        "ArgoCD",
        "Operator-sdk",
        "Kubespray",
        "Rancher",
        "OpenShift"
  ],
  "release": [
        "stable",
        "canary",
        "beta",
        "alpha",
        "rc"
  ],
  "tier": [
    "frontend",
    "backend",
    "cache",
    "database",
    "api"
  ]
}

actual_node_labels = {
    "k8s-worker1": {"memory": "6", "cpu-type": "mips64", "gpu-type": "nvidia-tesla", "storage-type": "sshd"},
    "k8s-worker2": {"memory": "4", "cpu-type": "mips32", "gpu-type": "amd-rdnd", "storage-type": "sata"},
    "k8s-worker3": {"memory": "5", "cpu-type": "ppc32", "gpu-type": "nvidia-hopper", "storage-type": "hdd"},
    "k8s-worker4": {"memory": "3", "cpu-type": "arm64", "gpu-type": "amd-radeon", "storage-type": "hdd"},
    "k8s-worker5": {"memory": "4", "cpu-type": "mips32", "gpu-type": "amd-radeon", "storage-type": "sata"},
    "k8s-worker6": {"memory": "3", "cpu-type": "ppc64", "gpu-type": "nvidia-hopper", "storage-type": "hdd"},
    "k8s-worker7": {"memory": "5", "cpu-type": "arm32", "gpu-type": "amd-rdnd", "storage-type": "hdd"},
    "k8s-worker8": {"memory": "4", "cpu-type": "ppc32", "gpu-type": "amd-rdnd", "storage-type": "ssd"},
    "k8s-worker9": {"memory": "5", "cpu-type": "ppc64", "gpu-type": "amd-radeon", "storage-type": "hdd"},
    "k8s-worker10": {"memory": "4", "cpu-type": "arm32", "gpu-type": "nvidia-tesla", "storage-type": "sshd"},
    "k8s-worker11": {"memory": "5", "cpu-type": "mips32", "gpu-type": "nvidia-rtx", "storage-type": "hdd"},
    "k8s-worker12": {"memory": "3", "cpu-type": "ppc64", "gpu-type": "nvidia-tesla", "storage-type": "sshd"},
    "k8s-worker13": {"memory": "4", "cpu-type": "mips64", "gpu-type": "nvidia-tesla", "storage-type": "sshd"},
    "k8s-worker14": {"memory": "6", "cpu-type": "amd64", "gpu-type": "amd-radeon", "storage-type": "nvme"},
    "k8s-worker15": {"memory": "4", "cpu-type": "arm32", "gpu-type": "amd-radeon", "storage-type": "sata"},
    "k8s-worker16": {"memory": "3", "cpu-type": "arm64", "gpu-type": "amd-rdnd", "storage-type": "ssd"},
    "k8s-worker17": {"memory": "4", "cpu-type": "mips64", "gpu-type": "nvidia-tesla", "storage-type": "nvme"},
    "k8s-worker18": {"memory": "5", "cpu-type": "amd64", "gpu-type": "amd-rdnd", "storage-type": "hdd"},
    "k8s-worker19": {"memory": "3", "cpu-type": "arm32", "gpu-type": "nvidia-hopper", "storage-type": "sshd"},
    "k8s-worker20": {"memory": "4", "cpu-type": "mips32", "gpu-type": "nvidia-tesla", "storage-type": "sata"},
    "k8s-worker21": {"memory": "3", "cpu-type": "ppc64", "gpu-type": "amd-rdnd", "storage-type": "hdd"},
    "k8s-worker22": {"memory": "5", "cpu-type": "arm32", "gpu-type": "amd-rdnd", "storage-type": "sata"},
    "k8s-worker23": {"memory": "3", "cpu-type": "ppc32", "gpu-type": "nvidia-tesla", "storage-type": "nvme"},
    "k8s-worker24": {"memory": "6", "cpu-type": "ppc64", "gpu-type": "amd-radeon", "storage-type": "sata"},
    "k8s-worker25": {"memory": "4", "cpu-type": "ppc64", "gpu-type": "nvidia-rtx", "storage-type": "sshd"},
    "k8s-worker26": {"memory": "6", "cpu-type": "mips32", "gpu-type": "nvidia-hopper", "storage-type": "hdd"},
    "k8s-worker27": {"memory": "3", "cpu-type": "mips32", "gpu-type": "amd-rdnd", "storage-type": "hdd"},
    "k8s-worker28": {"memory": "5", "cpu-type": "ppc64", "gpu-type": "amd-rdnd", "storage-type": "nvme"},
    "k8s-worker29": {"memory": "3", "cpu-type": "amd64", "gpu-type": "nvidia-hopper", "storage-type": "ssd"},
    "k8s-worker30": {"memory": "6", "cpu-type": "amd64", "gpu-type": "amd-radeon", "storage-type": "hdd"},
    "k8s-worker31": {"memory": "5", "cpu-type": "mips32", "gpu-type": "nvidia-hopper", "storage-type": "ssd"},
    "k8s-worker32": {"memory": "3", "cpu-type": "arm64", "gpu-type": "nvidia-hopper", "storage-type": "nvme"},
    "k8s-worker33": {"memory": "5", "cpu-type": "mips32", "gpu-type": "amd-radeon", "storage-type": "sata"},
    "k8s-worker34": {"memory": "6", "cpu-type": "arm32", "gpu-type": "nvidia-hopper", "storage-type": "sata"},
    "k8s-worker35": {"memory": "4", "cpu-type": "mips64", "gpu-type": "nvidia-rtx", "storage-type": "sshd"},
    "k8s-worker36": {"memory": "6", "cpu-type": "ppc32", "gpu-type": "amd-rdnd", "storage-type": "hdd"},
    "k8s-worker37": {"memory": "3", "cpu-type": "ppc64", "gpu-type": "amd-rdnd", "storage-type": "ssd"},
    "k8s-worker38": {"memory": "6", "cpu-type": "arm32", "gpu-type": "amd-rdnd", "storage-type": "nvme"},
    "k8s-worker39": {"memory": "3", "cpu-type": "mips32", "gpu-type": "amd-rdnd", "storage-type": "sshd"},
    "k8s-worker40": {"memory": "4", "cpu-type": "amd64", "gpu-type": "amd-radeon", "storage-type": "nvme"}
}

# registry URL, replace <LOCAL_REGISTRY> with the IP or hostname of your local registry server
url = "Replace it with your URL:5000"


def generate_random_string(length=5):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# pod affinity 생성 함수
def generate_random_pod_affinity(service_name, pod_affinity_data, preferred_count, required_count):
    pod_affinity = {
        "preferredDuringSchedulingIgnoredDuringExecution": [],
        "requiredDuringSchedulingIgnoredDuringExecution": []
    }

    keys = list(pod_affinity_data.keys())
    used_keys = set()

    # preferredDuringSchedulingIgnoredDuringExecution generation part
    for _ in range(preferred_count):
        key = random.choice(keys)
        while key in used_keys:
            key = random.choice(keys)
        used_keys.add(key)

        if key == "instance":
            selected_value = f"{service_name}_{generate_random_string()}"
        elif key == "app":
            selected_value = service_name
        elif key == "version":
            selected_value = random.choice(services[service_name]["versions"])
        else:
            values = pod_affinity_data[key]
            selected_value = random.choice(values)

        pod_affinity["preferredDuringSchedulingIgnoredDuringExecution"].append(
            {
                "weight": random.randint(1, 100),
                "podAffinityTerm": {
                    "labelSelector": {
                        "matchExpressions": [{"key": key, "operator": "In", "values": [selected_value]}]
                    },
                    "topologyKey": "kubernetes.io/hostname"
                }
            }
        )

    # requiredDuringSchedulingIgnoredDuringExecution generation part
    for _ in range(required_count):
        key = random.choice(keys)
        while key in used_keys:
            key = random.choice(keys)
        used_keys.add(key)

        if key == "instance":
            selected_value = f"{service_name}_{generate_random_string()}"
        elif key == "app":
            selected_value = service_name
        elif key == "version":
            selected_value = random.choice(services[service_name]["versions"])
        else:
            values = pod_affinity_data[key]
            selected_value = random.choice(values)

        pod_affinity["requiredDuringSchedulingIgnoredDuringExecution"].append(
            {
                "labelSelector": {
                    "matchExpressions": [{"key": key, "operator": "In", "values": [selected_value]}]
                },
                "topologyKey": "kubernetes.io/hostname"
            }
        )

    return pod_affinity

# node affinity
def generate_random_node_affinity(nodes, required_count):
    node_affinity = {
        "requiredDuringSchedulingIgnoredDuringExecution": {
            "nodeSelectorTerms": []
        }
    }

    available_nodes = list(nodes.keys())
    random.shuffle(available_nodes)

    match_expressions = []
    for i in range(min(required_count, len(available_nodes))):
        node_name = available_nodes[i]
        selected_labels = nodes[node_name]

        selected_keys = random.sample(list(selected_labels.keys()), k=2)

        for key in selected_keys:
            match_expressions.append({
                "key": key,
                "operator": "In",
                "values": [selected_labels[key]]
            })

    node_affinity["requiredDuringSchedulingIgnoredDuringExecution"]["nodeSelectorTerms"].append(
        {"matchExpressions": match_expressions}
    )

    return node_affinity

# function to extract label values from generated Affinity conditions
def extract_labels_from_affinity(pod_affinity):
    labels = {}
    for term in pod_affinity["preferredDuringSchedulingIgnoredDuringExecution"]:
        expr = term["podAffinityTerm"]["labelSelector"]["matchExpressions"][0]
        labels[expr["key"]] = expr["values"][0]
    for term in pod_affinity["requiredDuringSchedulingIgnoredDuringExecution"]:
        expr = term["labelSelector"]["matchExpressions"][0]
        labels[expr["key"]] = expr["values"][0]
    return labels

# Pod YAML Format Function
def create_pod_manifest(name, pod_affinity, version_list, service_name):
    # Affinity에서 version 정보를 가져옴
    labels = extract_labels_from_affinity(pod_affinity)  # Affinity로부터 라벨 추출
    selected_version = labels.get('version', None)

    # version info exception
    if selected_version is None:
        selected_version = random.choice(version_list)

    service_ports = {
        "registry": 5000,
        "httpd": 80,
        "memcached": 11211,
        "rabbitmq": 5672,
        "sonarqube": 9000,
        "elasticsearch": 9200,
        "caddy": 80,
        "eclipse-mosquitto": 1883,
        "vault": 8200,
        "mariadb": 3306,
        "mysql": 3306,
    }

    # generate pod manifests for each format by service
    if service_name in ["python", "node", "golang", "openjdk", "ruby", "maven"]:
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "labels": labels
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "command": ["tail", "-f", "/dev/null"],
                    }
                ]

            }
        }
    elif service_name == "busybox" :
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "labels": labels
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "command": ["sh", "-c", "echo Hello, Kubernetes! && sleep 3600"],
                    }
                ]

            }
        }
    elif service_name == "alpine" :
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "labels": labels
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "command": ["/bin/sh"],
                        "args": ["-c", "while true; do echo hello; sleep 10; done"],
                    }
                ]

            }
        }
    elif service_name in ["registry", "httpd", " memcached", "rabbitmq", "sonarqube", "elasticsearch", "caddy", "eclipse-mosquitto", "vault"] :
        image = f"{url}/{service_name}:{selected_version}"
        container_port = service_ports[service_name]
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "labels": labels
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "ports": [{"containerPort": container_port}]
                    }
                ]

            }
        }

    elif service_name in ["mysql", "mariadb"] :
        image = f"{url}/{service_name}:{selected_version}"
        container_port = service_ports[service_name]

        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "labels": labels
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "ports": [{"containerPort": container_port}],
                        "env": [
                            {"name": "ROOT", "value": "rootpassword"}  # 환경 변수 설정
                        ]
                    }
                ]
            }
        }

    else:
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "labels": labels
            },
            "spec": {
                "containers": [
                    {
                        "name": service_name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                    }
                ]
            }
        }

    return pod_manifest


def create_pod_manifest_with_affinity(name, pod_affinity, node_affinity, version_list, service_name):
    labels = extract_labels_from_affinity(pod_affinity)
    selected_version = labels.get('version', None)

    # version info exception
    if selected_version is None:
        selected_version = random.choice(version_list)

    service_ports = {
        "registry": 5000,
        "httpd": 80,
        "memcached": 11211,
        "rabbitmq": 5672,
        "sonarqube": 9000,
        "elasticsearch": 9200,
        "caddy": 80,
        "eclipse-mosquitto": 1883,
        "vault": 8200,
        "mariadb": 3306,
        "mysql": 3306,
    }

    # generate pod manifests for each format by service
    if service_name in ["python", "node", "golang", "openjdk", "ruby", "maven"]:
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "command": ["tail", "-f", "/dev/null"],
                    }
                ],
                "affinity": {
                    "nodeAffinity": node_affinity,
                    "podAffinity": pod_affinity
                }
            }
        }
    elif service_name == "busybox" :
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "command": ["sh", "-c", "echo Hello, Kubernetes! && sleep 3600"],
                    }
                ],
                "affinity": {
                    "nodeAffinity": node_affinity,
                    "podAffinity": pod_affinity
                }
            }
        }
    elif service_name == "alpine" :
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "command": ["/bin/sh"],
                        "args": ["-c", "while true; do echo hello; sleep 10; done"],
                    }
                ],
                "affinity": {
                    "nodeAffinity": node_affinity,
                    "podAffinity": pod_affinity
                }
            }
        }
    elif service_name in ["registry", "httpd", " memcached", "rabbitmq", "sonarqube", "elasticsearch", "caddy", "eclipse-mosquitto", "vault"] :
        image = f"{url}/{service_name}:{selected_version}"
        container_port = service_ports[service_name]
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "ports": [{"containerPort": container_port}]
                    }
                ],
                "affinity": {
                    "nodeAffinity": node_affinity,
                    "podAffinity": pod_affinity
                }
            }
        }

    elif service_name in ["mysql", "mariadb"] :
        image = f"{url}/{service_name}:{selected_version}"
        container_port = service_ports[service_name]

        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name
            },
            "spec": {
                "containers": [
                    {
                        "name": name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                        "ports": [{"containerPort": container_port}],
                        "env": [
                            {"name": "ROOT", "value": "rootpassword"}  # 환경 변수 설정
                        ]
                    }
                ],
                "affinity": {
                    "nodeAffinity": node_affinity,
                    "podAffinity": pod_affinity
                }
            }
        }

    else:
        image = f"{url}/{service_name}:{selected_version}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name
            },
            "spec": {
                "containers": [
                    {
                        "name": service_name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent",
                    }
                ],
                "affinity": {
                    "nodeAffinity": node_affinity,
                    "podAffinity": pod_affinity
                }
            }
        }

    return pod_manifest




# Number of attack pods to generate
N = 5
for service, config in services.items():
    for i in range(N):
        pod_name = f"{service}-pod-{i + 1}"

        pod_affinity = generate_random_pod_affinity(service, pod_affinity_data, preferred_count=2, required_count=1)

        # === PodBeater experiment variants ===
        # Tr tests (PodBeater_v3 / PodBeater_v5):
        #   Use this line (podAffinity only).
        pod_manifest = create_pod_manifest(pod_name, pod_affinity, config["versions"], service)

        # Tu tests (PodBeater_same / PodBeater_random):
        #   Comment out the above line,
        #   and instead uncomment the following two lines (nodeAffinity + podAffinity).
        #
        # node_affinity = generate_random_node_affinity(actual_node_labels, required_count=1)
        # pod_manifest = create_pod_manifest_with_affinity(pod_name, pod_affinity, node_affinity, config["versions"], service)
        # =====================================


        file_path = os.path.join(output_dir, f"{pod_name}.yaml")
        with open(file_path, "w") as file:
            yaml.dump(pod_manifest, file)

    print(f"{N} {service} Pod manifests for each service were created in the {output_dir} directory.")
