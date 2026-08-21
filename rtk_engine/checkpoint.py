import json
import os
import time

PATH = "results/checkpoints/latest.json"


def save_checkpoint(done, metadata=None):
    os.makedirs("results/checkpoints", exist_ok=True)
    payload = {
        "completed": done,
        "timestamp": time.time(),
        "metadata": metadata or {},
    }
    with open(PATH, "w") as f:
        json.dump(payload, f, indent=2)


def load_checkpoint():
    if not os.path.exists(PATH):
        return 0
    with open(PATH) as f:
        return json.load(f).get("completed", 0)
