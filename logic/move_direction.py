from dataclasses import dataclass

from .coord import Coord


@dataclass
class MoveDirection:
    d_r: int
    d_c: int

    def apply(self, coord: Coord):
        return Coord(coord.r + self.d_r, coord.c + self.d_c)

