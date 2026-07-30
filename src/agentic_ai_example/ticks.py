"""Nice tick locations and labels for a fixed character grid.

This is the classic "nice numbers" problem: pick round values (multiples of
1, 2, 2.5, or 5 times a power of ten) that cover a data range without
exceeding the number of ticks that fit on screen.
"""

from __future__ import annotations

import math

__all__ = ["format_ticks", "nice_ticks"]

_NICE_STEPS = (1.0, 2.0, 2.5, 5.0, 10.0)


def nice_ticks(lo: float, hi: float, max_ticks: int) -> list[float]:
    """Return at most ``max_ticks`` round values inside [lo, hi].

    Requires ``lo < hi``. The result may be empty for very tight ranges.
    """
    raw = (hi - lo) / max(max_ticks - 1, 1)
    mag = 10.0 ** math.floor(math.log10(raw))
    frac = raw / mag
    # Snap *up* to the next nice step so the tick count never exceeds max_ticks.
    snap = next((s for s in _NICE_STEPS if s >= frac), 10.0)
    step = snap * mag
    # Enough digits to represent the step; rounding kills float noise.
    ndigits = max(0, -math.floor(math.log10(step))) + 1
    ticks = []
    k = math.ceil(lo / step)
    while k * step <= hi + step * 1e-9:
        ticks.append(round(k * step, ndigits))
        k += 1
    return ticks


def format_ticks(ticks: list[float]) -> list[str]:
    """Format ticks with one shared format so label widths are predictable."""
    if all(t == int(t) for t in ticks):
        return [f"{t:g}" for t in ticks]
    step = abs(ticks[1] - ticks[0]) if len(ticks) > 1 else abs(ticks[0])
    decimals = 0
    while decimals < 10 and abs(step * 10**decimals - round(step * 10**decimals)) > 1e-9:
        decimals += 1
    return [f"{t:.{decimals}f}" for t in ticks]
