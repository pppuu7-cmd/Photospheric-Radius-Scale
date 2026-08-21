from multiprocessing import Pool, cpu_count
import time

from .config import *
from .worker import calculate
from .progress import show_progress
from .checkpoint import save_checkpoint, load_checkpoint


def main():
    workers = min(cpu_count() - CPU_RESERVED, MAX_WORKERS)
    start_index = load_checkpoint()

    print("RTK Parallel Engine v1")
    print(f"Workers: {workers}")
    print(f"Resume: {start_index}")

    start = time.time()

    with Pool(workers) as pool:
        for i, _ in enumerate(
            pool.imap(calculate, range(start_index, TOTAL_TASKS)),
            start=start_index,
        ):
            if i % PROGRESS_INTERVAL == 0:
                show_progress(i, TOTAL_TASKS, start)
            if i % CHECKPOINT_INTERVAL == 0:
                save_checkpoint(i, {"workers": workers})

    save_checkpoint(TOTAL_TASKS, {"workers": workers, "status": "complete"})
    print("\nDONE")


if __name__ == "__main__":
    main()
