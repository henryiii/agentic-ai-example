from __future__ import annotations

import re

from agentic_ai_example import Figure

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def strip(s: str) -> str:
    return ANSI.sub("", s)


def test_line_figure():
    fig = Figure(width=40, height=12, title="lines")
    fig.ax.plot([0, 5, 10], [0, 5, 0])
    out = strip(str(fig))
    lines = out.split("\n")
    assert len(lines) == 12
    assert all(len(line) == 40 for line in lines)
    assert "lines" in lines[0]
    assert "●" in out
    assert "│" in out
    assert "└" in out
    assert "10" in out  # x tick label


def test_horizontal_line_row():
    fig = Figure(width=30, height=9)
    fig.ax.plot([0, 1], [1, 1])
    out = strip(str(fig))
    marker_rows = [i for i, line in enumerate(out.split("\n")) if "●" in line]
    assert len(marker_rows) == 1  # a flat line stays on one row


def test_bar_figure():
    fig = Figure(width=40, height=12)
    fig.ax.bar([3, 1, 2])
    out = strip(str(fig))
    assert "█" in out
    assert "0" in out and "2" in out  # nice_ticks(0, 3, 3) -> [0, 2]


def test_imshow_figure():
    fig = Figure(width=30, height=10)
    fig.ax.imshow([[0.0, 1.0], [1.0, 0.0]])
    raw = str(fig)
    assert "▀" in raw
    assert "\x1b[38;2;" in raw
    assert "\x1b[48;2;" in raw
    assert strip(raw).count("\n") == 9
