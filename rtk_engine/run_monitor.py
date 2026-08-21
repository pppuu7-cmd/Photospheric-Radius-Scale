import json
import os
import time

CHECKPOINT = "results/checkpoints/latest.json"


def monitor(interval=10):
    print("RTK monitor started")
    while True:
        if os.path.exists(CHECKPOINT):
            with open(CHECKPOINT) as f:
                state = json.load(f)
            print(
                f"completed={state.get('completed')} "
                f"status={state.get('metadata', {}).get('status', 'running')}"
            )
        else:
            print("waiting for checkpoint")
        time.sleep(interval)


if __name__ == "__main__":
    monitor()
