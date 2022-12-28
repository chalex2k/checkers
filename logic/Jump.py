from dataclasses import dataclass
from typing import Optional

from .coord import Coord
from .figures import Figure


@dataclass
class Jump:
    """ Один шаг взятия"""

    from_: Coord
    to: Coord
    was_taken: Optional[Figure] = None

    @property
    def taken_coord(self):
        return Coord((self.from_.r + self.to.r)//2, (self.from_.c + self.to.c)//2)


@dataclass
class Take:
    figure: Figure
    jumps: list[Jump]
    field_before: list[list[Figure]]
