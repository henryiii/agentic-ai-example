"""Plot artists: things that know their data bounds and how to draw cells."""

from __future__ import annotations

import abc
import dataclasses
import itertools
from typing import TYPE_CHECKING

from .colormap import VIRIDIS, Colormap

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .canvas import RGB, Canvas

__all__ = ["Artist", "Bars", "Bounds", "HeatMap", "Line", "Transform"]

Bounds = tuple[float, float, float, float]  # xmin, xmax, ymin, ymax

_BLOCKS = " ▁▂▃▄▅▆▇█"


@dataclasses.dataclass(frozen=True)
class Transform:
    """Linear map from data coordinates to a rectangle of character cells.

    Data values map to cell *centers*: xmin -> col0 and ymax -> row0 (rows
    grow downward on screen, so the y axis is flipped here).
    """

    xmin: float
    xmax: float
    ymin: float
    ymax: float
    col0: int
    row0: int
    width: int
    height: int

    def col(self, x: float) -> int:
        return self.col0 + round(
            (x - self.xmin) / (self.xmax - self.xmin) * (self.width - 1)
        )

    def rowf(self, y: float) -> float:
        return self.row0 + (self.ymax - y) / (self.ymax - self.ymin) * (self.height - 1)

    def row(self, y: float) -> int:
        return round(self.rowf(y))


class Artist(abc.ABC):
    """Base class for anything an Axes can draw."""

    @abc.abstractmethod
    def bounds(self) -> Bounds:
        """Data limits this artist needs: (xmin, xmax, ymin, ymax)."""

    @abc.abstractmethod
    def draw(self, canvas: Canvas, t: Transform) -> None:
        """Draw onto the canvas using the data-to-cell transform."""


@dataclasses.dataclass
class Line(Artist):
    """A line plot: markers at each point, connected cell-by-cell."""

    xs: Sequence[float]
    ys: Sequence[float]
    color: RGB | None = None
    marker: str = "●"

    def bounds(self) -> Bounds:
        return (min(self.xs), max(self.xs), min(self.ys), max(self.ys))

    def draw(self, canvas: Canvas, t: Transform) -> None:
        cells = [(t.col(x), t.row(y)) for x, y in zip(self.xs, self.ys, strict=True)]
        for (c0, r0), (c1, r1) in itertools.pairwise(cells):
            steps = max(abs(c1 - c0), abs(r1 - r0), 1)
            for i in range(steps + 1):
                col = round(c0 + (c1 - c0) * i / steps)
                row = round(r0 + (r1 - r0) * i / steps)
                canvas.put(col, row, self.marker, fg=self.color)


@dataclasses.dataclass
class Bars(Artist):
    """A vertical bar plot of non-negative heights, one bar per category."""

    heights: Sequence[float]
    color: RGB | None = None

    def bounds(self) -> Bounds:
        return (-0.5, len(self.heights) - 0.5, 0.0, max(self.heights))

    def draw(self, canvas: Canvas, t: Transform) -> None:
        n = len(self.heights)
        bar_w = max(1, t.width // n - 1)
        base = t.row(0.0)
        for i, h in enumerate(self.heights):
            # Bars rise from the bottom edge of the baseline row to the
            # row center of the value, hence the extra half cell.
            length = t.rowf(0.0) - t.rowf(h) + 0.5
            full, frac = int(length), length - int(length)
            start = t.col(i) - bar_w // 2
            for dc in range(bar_w):
                for k in range(full):
                    canvas.put(start + dc, base - k, "█", fg=self.color)
                eighths = round(frac * 8)
                if eighths:
                    canvas.put(start + dc, base - full, _BLOCKS[eighths], fg=self.color)


@dataclasses.dataclass
class HeatMap(Artist):
    """An imshow-style image: two vertical pixels per cell via ▀ fg/bg colors."""

    values: Sequence[Sequence[float]]
    cmap: Colormap = VIRIDIS

    def bounds(self) -> Bounds:
        return (0.0, float(len(self.values[0])), 0.0, float(len(self.values)))

    def draw(self, canvas: Canvas, t: Transform) -> None:
        lo = min(min(row) for row in self.values)
        hi = max(max(row) for row in self.values)
        span = (hi - lo) or 1.0
        nrows, ncols = len(self.values), len(self.values[0])
        px_h = t.height * 2
        for r in range(t.height):
            for c in range(t.width):
                sx = int(c / t.width * ncols)
                top_sy = int(r * 2 / px_h * nrows)
                bot_sy = int((r * 2 + 1) / px_h * nrows)
                top = (self.values[top_sy][sx] - lo) / span
                bot = (self.values[bot_sy][sx] - lo) / span
                canvas.put(
                    t.col0 + c, t.row0 + r, "▀", fg=self.cmap(top), bg=self.cmap(bot)
                )
