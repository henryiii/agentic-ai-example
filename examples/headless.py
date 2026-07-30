"""Drive the demo app headless and print the resulting screen.

Run with: uv run --group examples python examples/headless.py --keys 2,plus

Key names follow Textual conventions: 1, 2, 3, plus, minus, q.
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from app import PlotApp, screen_text


async def run(size: tuple[int, int], keys: list[str], *, ansi: bool) -> str:
    app = PlotApp()
    async with app.run_test(size=size) as pilot:
        if keys:
            await pilot.press(*keys)
        await pilot.pause()
        return screen_text(app, styles=ansi)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", default="80x24", help="terminal size as WIDTHxHEIGHT")
    parser.add_argument("--keys", default="", help="comma-separated keys to press")
    parser.add_argument("--ansi", action="store_true", help="keep ANSI color codes")
    args = parser.parse_args(argv)

    width, _, height = args.size.partition("x")
    keys = [key for key in args.keys.split(",") if key]
    text = asyncio.run(run((int(width), int(height)), keys, ansi=args.ansi))
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
