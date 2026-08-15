"""Minimal colormaps: linear interpolation over evenly spaced RGB points."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .canvas import RGB

__all__ = ["VIRIDIS", "Colormap"]


class Colormap:
    """Map a value in [0, 1] to an RGB color."""

    def __init__(self, points: Sequence[RGB]) -> None:
        self.points = list(points)

    def __call__(self, t: float) -> RGB:
        t = min(max(t, 0.0), 1.0)
        pos = t * (len(self.points) - 1)
        i = min(int(pos), len(self.points) - 2)
        frac = pos - i
        a, b = self.points[i], self.points[i + 1]
        return (
            round(a[0] + (b[0] - a[0]) * frac),
            round(a[1] + (b[1] - a[1]) * frac),
            round(a[2] + (b[2] - a[2]) * frac),
        )


VIRIDIS = Colormap(
    [(68, 1, 84), (59, 82, 139), (33, 145, 140), (94, 201, 98), (253, 231, 37)]
)
