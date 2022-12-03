from dataclasses import dataclass
from typing import Optional

from .coord import Coord
from .figures import Figure


@dataclass
class Take:
    figure: Figure
    from_: Coord
    to: Coord
    was_taken: Optional[Figure] = None

    @property
    def taken_coord(self):
        return Coord((self.from_.r + self.to.r)//2, (self.from_.c + self.to.c)//2)
