"""Figure and Axes: layout, limits, and frame drawing."""

from __future__ import annotations

from collections.abc import Sequence

from .artists import Artist, Bars, Bounds, HeatMap, Line, Transform
from .canvas import RGB, Canvas
from .colormap import VIRIDIS, Colormap
from .ticks import format_ticks, nice_ticks

__all__ = ["Axes", "Figure"]


class Axes:
    """A single plot area: collects artists, computes limits, draws the frame."""

    def __init__(self) -> None:
        self.artists: list[Artist] = []

    def plot(
        self, xs: Sequence[float], ys: Sequence[float], color: RGB | None = None
    ) -> None:
        """Add a line plot."""
        self.artists.append(Line(list(xs), list(ys), color))

    def bar(self, heights: Sequence[float], color: RGB | None = None) -> None:
        """Add a bar plot of non-negative heights."""
        self.artists.append(Bars(list(heights), color))

    def imshow(
        self, values: Sequence[Sequence[float]], cmap: Colormap = VIRIDIS
    ) -> None:
        """Add an image plot of a 2D array, colored by the colormap."""
        self.artists.append(HeatMap([list(row) for row in values], cmap))

    def _limits(self) -> Bounds:
        if not self.artists:
            return (0.0, 1.0, 0.0, 1.0)
        bs = [a.bounds() for a in self.artists]
        xmin, xmax = min(b[0] for b in bs), max(b[1] for b in bs)
        ymin, ymax = min(b[2] for b in bs), max(b[3] for b in bs)
        if all(isinstance(a, Line) for a in self.artists):
            margin = 0.05 * (ymax - ymin)
            ymin, ymax = ymin - margin, ymax + margin
        if xmin == xmax:
            xmin, xmax = xmin - 0.5, xmax + 0.5
        if ymin == ymax:
            ymin, ymax = ymin - 0.5, ymax + 0.5
        return (xmin, xmax, ymin, ymax)

    def render(self, canvas: Canvas, top: int = 0) -> None:
        """Draw frame, ticks, labels, and artists onto rows [top, height)."""
        xmin, xmax, ymin, ymax = self._limits()
        # Reserve one row for the bottom spine and one for the x tick labels.
        plot_h = canvas.height - top - 2
        yticks = nice_ticks(ymin, ymax, max(2, plot_h // 3))
        ylabels = format_ticks(yticks)
        gutter = max((len(label) for label in ylabels), default=1)
        plot_w = canvas.width - gutter - 1
        t = Transform(xmin, xmax, ymin, ymax, gutter + 1, top, plot_w, plot_h)

        bottom = top + plot_h
        for r in range(plot_h):
            canvas.put(gutter, top + r, "│")
        canvas.put(gutter, bottom, "└")
        for c in range(plot_w):
            canvas.put(gutter + 1 + c, bottom, "─")

        for tick, label in zip(yticks, ylabels, strict=True):
            r = t.row(tick)
            canvas.put(gutter, r, "┤")
            canvas.text(gutter - len(label), r, label)

        xticks = nice_ticks(xmin, xmax, max(2, plot_w // 8))
        xlabels = format_ticks(xticks)
        last_end = -2
        for tick, label in zip(xticks, xlabels, strict=True):
            c = t.col(tick)
            canvas.put(c, bottom, "┬")
            start = min(max(c - len(label) // 2, 0), canvas.width - len(label))
            if start <= last_end + 1:  # greedy skip of overlapping labels
                continue
            canvas.text(start, bottom + 1, label)
            last_end = start + len(label) - 1

        for artist in self.artists:
            artist.draw(canvas, t)


class Figure:
    """A fixed-size figure holding one Axes. ``print(fig)`` renders it."""

    def __init__(
        self, width: int = 72, height: int = 20, title: str | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.title = title
        self._ax = Axes()

    @property
    def ax(self) -> Axes:
        """The figure's single Axes."""
        return self._ax

    def render(self) -> str:
        """Render the full figure to a string with ANSI colors."""
        canvas = Canvas(self.width, self.height)
        top = 0
        if self.title:
            canvas.text(max((self.width - len(self.title)) // 2, 0), 0, self.title)
            top = 1
        self._ax.render(canvas, top)
        return canvas.render()

    def __str__(self) -> str:
        return self.render()
