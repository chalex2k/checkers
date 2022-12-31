from dataclasses import dataclass
from typing import Optional

from logic.cell import Cell
from .coord import Coord


@dataclass
class Jump:
    """ Один шаг взятия"""
    from_: Coord
    to: Coord
    was_taken: Optional[Cell] = None

    @property
    def taken_coord(self):
        for r, c in zip(range(self.from_.r, self.to.r, (self.to.r - self.from_.r) // abs(self.to.r - self.from_.r)),
                        range(self.from_.c, self.to.c, (self.to.c - self.from_.c) // abs(self.to.c - self.from_.c))):
            yield Coord(r, c)


@dataclass
class Take:
    figure: Cell
    jumps: list[Jump]
    field_before: list[list[Cell]]



    def __str__(self):
        literal = 'B' if self.figure.is_black else 'W'
        return f'T({literal}:{self.jumps[0].from_}->{self.jumps[-1].to})'

