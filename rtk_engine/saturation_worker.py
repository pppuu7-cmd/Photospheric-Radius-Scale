"""Synthetic CPU-bound worker used only to validate home-node saturation.

This module is infrastructure-only. It must never be interpreted as an RTK
scientific calculation.
"""

from __future__ import annotations

import os
import time

TARGET_SECONDS = float(os.getenv("RTK_SATURATION_SECONDS", "8"))


def calculate(index: int) -> int:
    """Burn one CPU continuously for a controlled wall-clock interval."""
    deadline = time.perf_counter() + max(0.1, TARGET_SECONDS)
    x = (int(index) + 1) & 0xFFFFFFFFFFFFFFFF
    while time.perf_counter() < deadline:
        # Check the clock only once per block so nearly all time is arithmetic.
        for _ in range(20_000):
            x = (x * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
            x ^= (x >> 17)
    return x
