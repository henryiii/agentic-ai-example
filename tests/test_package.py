from __future__ import annotations

import importlib.metadata

import agentic_ai_example as m


def test_version() -> None:
    assert importlib.metadata.version("agentic_ai_example") == m.__version__
