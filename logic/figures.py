from dataclasses import dataclass

from logic.color import Color
from logic.move_direction import MoveDirection
from logic.take_direction import TakeDirection


class Figure:
    pass


@dataclass
class Checker(Figure):
    color: Color

    _checkers_directions_moves = {
        Color.WHITE: [MoveDirection(d_r=-1, d_c=-1), MoveDirection(d_r=-1, d_c=+1)],
        Color.BLACK: [MoveDirection(d_r=+1, d_c=-1), MoveDirection(d_r=+1, d_c=+1)]
    }

    _checkers_directions_takes = [TakeDirection(d_r=-2, d_c=-2), TakeDirection(d_r=-2, d_c=+2),
                                  TakeDirection(d_r=2, d_c=-2), TakeDirection(d_r=2, d_c=+2)]

    @property
    def directions_moves(self):
        return self._checkers_directions_moves[self.color]

    @property
    def directions_takes(self):
        return self._checkers_directions_takes


@dataclass
class Queen(Figure):
    color: Color


class Empty(Figure):
    pass
