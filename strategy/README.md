# 📁 strategy/

This folder contains the PodBeater attack pod generation scripts used for generating attack pod manifests under different threat models. 

--

## 📄 Contents

- `PodBeater_same.py`      — Tu scenario: extend the victim pod’s scheduling requirements with additional values- 
- `PodBeater_random.py`    — Tu scenario: extend the victim pod’s scheduling requirements with new values each attempt  
- `PodBeater_Tr.py`        — Tr scenario: generate attack pods with multi-value affinity (use `--multi-value N`)


#### Threat model **Tu** (attacker *knows* victim scheduling requirements)

```bash
# Run PodBeater_same.py
python3 strategy/PodBeater_same.py <path/to/target_pod_yaml> <path/to/output_attack_pod_yaml>

# Run PodBeater_random.py
python3 strategy/PodBeater_random.py <path/to/target_pod_yaml> <path/to/attack_pods_output_directory>
```

#### Threat model **Tr** (attacker *does not know* victim scheduling requirements)
```bash
# PodBeater_v3 behavior
python3 PodBeater_Tr.py --multi-value 3 --out-dir attack_pods_v3

# PodBeater_v5 behavior 
python3 PodBeater_Tr.py --multi-value 5 --out-dir attack_pods_v5
```
