"""Pilot-driven tests for the Textual demo app (skipped if textual is not installed)."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

pytest.importorskip("textual")

sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))

from app import PlotApp, PlotView, screen_text

SIZE = (80, 24)


def test_initial_screen():
    async def scenario() -> str:
        app = PlotApp()
        async with app.run_test(size=SIZE) as pilot:
            await pilot.pause()
            return str(screen_text(app))

    text = asyncio.run(scenario())
    assert "sin(2x)" in text


def test_switch_kind_and_param():
    async def scenario() -> tuple[str, PlotView]:
        app = PlotApp()
        async with app.run_test(size=SIZE) as pilot:
            await pilot.press("2", "plus")
            await pilot.pause()
            return str(screen_text(app)), app.query_one(PlotView)

    text, view = asyncio.run(scenario())
    assert view.kind == "bar"
    assert view.param == 3
    assert "9 bars" in text


def test_param_floor():
    async def scenario() -> PlotView:
        app = PlotApp()
        async with app.run_test(size=SIZE) as pilot:
            await pilot.press("minus", "minus", "minus")
            await pilot.pause()
            return app.query_one(PlotView)

    view = asyncio.run(scenario())
    assert view.param == 1


def test_initial_state_arguments():
    async def scenario() -> str:
        app = PlotApp(kind="heat", param=1)
        async with app.run_test(size=SIZE) as pilot:
            await pilot.pause()
            return str(screen_text(app))

    text = asyncio.run(scenario())
    assert "sin(x)·cos(y)" in text
