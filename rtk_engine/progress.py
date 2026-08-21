import time


def show_progress(done, total, start_time):
    percent = done / total * 100 if total else 100
    elapsed = time.time() - start_time
    speed = done / elapsed if elapsed else 0
    eta = (total - done) / speed if speed else 0

    width = 30
    filled = int(width * percent / 100)
    bar = "#" * filled + "-" * (width - filled)

    print(
        f"\r[{bar}] {percent:5.1f}% "
        f"{done}/{total} "
        f"speed={speed:.0f}/s "
        f"ETA={eta/60:.1f}min",
        end="",
        flush=True,
    )
