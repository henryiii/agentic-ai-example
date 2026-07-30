from __future__ import annotations

from agentic_ai_example.canvas import Canvas


def test_render_plain():
    canvas = Canvas(3, 2)
    canvas.text(0, 0, "ab")
    canvas.put(2, 1, "x")
    assert canvas.render() == "ab \n  x"


def test_out_of_range_is_noop():
    canvas = Canvas(2, 2)
    canvas.put(-1, 0, "x")
    canvas.put(0, 5, "x")
    canvas.put(2, 0, "x")
    assert canvas.render() == "  \n  "


def test_colors_set_and_reset():
    canvas = Canvas(2, 1)
    canvas.put(0, 0, "a", fg=(1, 2, 3))
    out = canvas.render()
    assert out == "\x1b[38;2;1;2;3ma\x1b[0m "


def test_background_color():
    canvas = Canvas(1, 1)
    canvas.put(0, 0, "▀", fg=(1, 2, 3), bg=(4, 5, 6))
    out = canvas.render()
    assert "\x1b[38;2;1;2;3m" in out
    assert "\x1b[48;2;4;5;6m" in out
    assert out.endswith("\x1b[0m")
