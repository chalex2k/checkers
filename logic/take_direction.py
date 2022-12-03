from dataclasses import dataclass

from .coord import Coord


@dataclass
class TakeDirection:
    d_r: int
    d_c: int

    def apply(self, coord: Coord):
        return Coord(coord.r + self.d_r, coord.c + self.d_c)

    def taken(self, coord: Coord):
        return Coord(coord.r + self.d_r // 2, coord.c + self.d_c // 2)

    def __add__(self, other):
        if self.d_r + other.d_r == 0 and self.d_c + other.d_c == 0:
            return 0
        else:
            return other
