from __future__ import annotations

import itertools

import pytest

from agentic_ai_example.ticks import format_ticks, nice_ticks


def test_simple_range():
    assert nice_ticks(0, 10, 6) == [0, 2, 4, 6, 8, 10]


def test_quarter_steps():
    assert nice_ticks(0, 1, 5) == [0, 0.25, 0.5, 0.75, 1.0]


def test_snap_to_larger_step():
    assert nice_ticks(0, 100, 6) == [0, 20, 40, 60, 80, 100]


def test_negative_range():
    assert nice_ticks(-1.2, 1.2, 5) == [-1, 0, 1]


def test_lo_off_step_boundary():
    assert nice_ticks(0.3, 9.7, 6) == [2, 4, 6, 8]


@pytest.mark.parametrize(
    ("lo", "hi"),
    [(0, 10), (-5, 3), (0.001, 0.0027), (12345, 12389), (-2.5, -1.0)],
)
@pytest.mark.parametrize("max_ticks", [2, 5, 10])
def test_tick_properties(lo, hi, max_ticks):
    ticks = nice_ticks(lo, hi, max_ticks)
    span = hi - lo
    assert len(ticks) <= max_ticks
    assert all(lo - 1e-9 * span <= t <= hi + 1e-9 * span for t in ticks)
    steps = [b - a for a, b in itertools.pairwise(ticks)]
    assert all(step == pytest.approx(steps[0]) for step in steps)


def test_format_integral():
    assert format_ticks([0.0, 2.0, 4.0]) == ["0", "2", "4"]


def test_format_fractional():
    assert format_ticks([0.0, 0.25, 0.5]) == ["0.00", "0.25", "0.50"]


def test_format_float_noise():
    assert format_ticks([0.1, 0.2, 0.30000000000000004]) == ["0.1", "0.2", "0.3"]
