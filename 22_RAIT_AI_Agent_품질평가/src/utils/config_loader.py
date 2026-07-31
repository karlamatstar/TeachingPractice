import json
import os

def load_policy(policy_name="default_pilot"):
    config_path = os.path.join("config", "policy_config.json")
    if not os.path.exists(config_path):
        # 파일이 없을 경우 폴더 및 기본값 자동 생성
        os.makedirs("config", exist_ok=True)
        default_config = {
            "default_pilot": {
                "target_score": 3.5,
                "cutoffs": {"S": 3.0, "A": 3.0},
                "weights": {"R": 1, "E": 1, "U": 1, "S": 1, "T": 1, "A": 1, "C": 1, "P": 1}
            }
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)
        return default_config["default_pilot"]

    with open(config_path, "r", encoding="utf-8") as f:
        policies = json.load(f)
    return policies.get(policy_name, policies["default_pilot"])