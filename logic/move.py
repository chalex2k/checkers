from dataclasses import dataclass

from logic.cell import Cell
from .coord import Coord


@dataclass
class Move:
    checker: Cell
    from_: Coord
    to: Coord
    field_before: list[list[Cell]]

    def __str__(self):
        literal = 'B' if self.checker.is_black else 'W'
        return f'M({literal}:{self.from_}->{self.to})'

