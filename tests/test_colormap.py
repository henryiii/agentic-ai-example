from __future__ import annotations

from agentic_ai_example.colormap import VIRIDIS, Colormap


def test_endpoints():
    assert VIRIDIS(0.0) == (68, 1, 84)
    assert VIRIDIS(1.0) == (253, 231, 37)


def test_clamping():
    assert VIRIDIS(-3.0) == VIRIDIS(0.0)
    assert VIRIDIS(2.0) == VIRIDIS(1.0)


def test_midpoint_lerp():
    cmap = Colormap([(0, 0, 0), (100, 50, 200)])
    assert cmap(0.5) == (50, 25, 100)
