"""A grid of character cells that renders to a string with ANSI colors."""

from __future__ import annotations

import dataclasses

__all__ = ["RGB", "Canvas", "Cell"]

RGB = tuple[int, int, int]

RESET = "\x1b[0m"


@dataclasses.dataclass
class Cell:
    """One character cell with optional foreground/background colors."""

    char: str = " "
    fg: RGB | None = None
    bg: RGB | None = None


class Canvas:
    """A fixed-size grid of cells. Column 0 is left, row 0 is top."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]

    def put(
        self,
        col: int,
        row: int,
        char: str,
        fg: RGB | None = None,
        bg: RGB | None = None,
    ) -> None:
        """Set one cell. Out-of-range coordinates are silently ignored."""
        if 0 <= col < self.width and 0 <= row < self.height:
            self.grid[row][col] = Cell(char, fg, bg)

    def text(self, col: int, row: int, string: str, fg: RGB | None = None) -> None:
        """Write a horizontal string starting at (col, row)."""
        for i, char in enumerate(string):
            self.put(col + i, row, char, fg)

    def render(self) -> str:
        """Render to a multi-line string, emitting color codes only on change."""
        lines = []
        for row in self.grid:
            parts = []
            current: tuple[RGB | None, RGB | None] = (None, None)
            for cell in row:
                colors = (cell.fg, cell.bg)
                if colors != current:
                    if current != (None, None):
                        parts.append(RESET)
                    if cell.fg is not None:
                        parts.append(
                            f"\x1b[38;2;{cell.fg[0]};{cell.fg[1]};{cell.fg[2]}m"
                        )
                    if cell.bg is not None:
                        parts.append(
                            f"\x1b[48;2;{cell.bg[0]};{cell.bg[1]};{cell.bg[2]}m"
                        )
                    current = colors
                parts.append(cell.char)
            if current != (None, None):
                parts.append(RESET)
            lines.append("".join(parts))
        return "\n".join(lines)
