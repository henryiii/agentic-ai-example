"""Copyright (c) 2026 Henry Schreiner. All rights reserved.

agentic-ai-example: An example project for a workshop

A tiny terminal plotting library: line plots, bar plots, and imshow-style
images rendered as ANSI-colored text.
"""

from __future__ import annotations

from .colormap import VIRIDIS, Colormap
from .figure import Axes, Figure

__version__ = "0.1.0"

__all__ = ["VIRIDIS", "Axes", "Colormap", "Figure", "__version__"]
