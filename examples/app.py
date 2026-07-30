"""Textual demo app for the terminal plotting library.

Run with: uv run --group examples python examples/app.py
"""

from __future__ import annotations

import io
import math
import typing

from rich.console import Console
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from agentic_ai_example import Figure


def build_figure(kind: str, param: int, width: int, height: int) -> Figure:
    if kind == "line":
        fig = Figure(width, height, title=f"sin({param}x)")
        xs = [i / 10 for i in range(101)]
        fig.ax.plot(xs, [math.sin(param * x) for x in xs], color=(255, 120, 120))
    elif kind == "bar":
        fig = Figure(width, height, title=f"{3 * param} bars")
        fig.ax.bar(
            [5 + 4 * math.sin(0.7 * i) for i in range(3 * param)], color=(120, 180, 255)
        )
    else:
        fig = Figure(width, height, title="sin(x)·cos(y)")
        n = 16 * param
        fig.ax.imshow(
            [
                [math.sin(x / n * 12) * math.cos(y / n * 6) for x in range(2 * n)]
                for y in range(n)
            ]
        )
    return fig


class PlotView(Static):
    def __init__(self, kind: str = "line", param: int = 2) -> None:
        super().__init__()
        self.kind = kind
        self.param = param

    def render(self) -> Text:
        width = max(self.size.width, 20)
        height = max(self.size.height, 8)
        return Text.from_ansi(str(build_figure(self.kind, self.param, width, height)))


class PlotApp(App[None]):
    BINDINGS: typing.ClassVar = [
        ("1", "kind('line')", "Line"),
        ("2", "kind('bar')", "Bars"),
        ("3", "kind('heat')", "Heatmap"),
        ("plus,equals_sign", "param(1)", "More"),
        ("minus", "param(-1)", "Less"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, kind: str = "line", param: int = 2) -> None:
        super().__init__()
        self._initial_kind = kind
        self._initial_param = param

    def compose(self) -> ComposeResult:
        yield Header()
        yield PlotView(self._initial_kind, self._initial_param)
        yield Footer()

    def action_kind(self, kind: str) -> None:
        view = self.query_one(PlotView)
        view.kind = kind
        view.refresh()

    def action_param(self, delta: int) -> None:
        view = self.query_one(PlotView)
        view.param = max(1, view.param + delta)
        view.refresh()


def screen_text(app: App[None], *, styles: bool = False) -> str:
    """Render the app's current screen to a string (ANSI codes if styles=True)."""
    console = Console(
        width=app.size.width,
        height=app.size.height,
        file=io.StringIO(),
        force_terminal=True,
        color_system="truecolor",
        record=True,
        legacy_windows=False,
        safe_box=False,
    )
    console.print(app.screen._compositor)
    return console.export_text(styles=styles)


if __name__ == "__main__":
    PlotApp().run()
