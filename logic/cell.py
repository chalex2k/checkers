from __future__ import annotations
from enum import Enum

from logic.move_direction import MoveDirection
from logic.take_direction import TakeDirection


class Cell(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = -1
    K_WHITE = 2
    K_BLACK = -2

    @property
    def is_black(self):
        return self in (self.BLACK, self.K_BLACK)

    @property
    def is_white(self):
        return self in (self.WHITE, self.K_WHITE)

    @property
    def is_checker(self):
        return self in (self.BLACK, self.WHITE)

    @property
    def is_queen(self):
        return self in (self.K_BLACK, self.K_WHITE)

    def same_color(self, cell: Cell) -> bool:
        return self != self.EMPTY and cell != self.EMPTY and self.is_white == cell.is_white

    def opposite_color(self, cell: Cell):
        return self != self.EMPTY and cell != self.EMPTY and self.is_white != cell.is_white

    @property
    def directions_moves(self) -> list[MoveDirection]:
        direction_moves_white = [MoveDirection(d_r=-1, d_c=-1), MoveDirection(d_r=-1, d_c=+1)]
        direction_moves_black = [MoveDirection(d_r=+1, d_c=-1), MoveDirection(d_r=+1, d_c=+1)]
        if self == self.WHITE:
            return direction_moves_white
        elif self == self.BLACK:
            return direction_moves_black
        elif self.is_queen:
            return direction_moves_white + direction_moves_black
        return []

    @property
    def directions_takes(self):
        return [TakeDirection(d_r=-2, d_c=-2), TakeDirection(d_r=-2, d_c=+2),
                TakeDirection(d_r=2, d_c=-2), TakeDirection(d_r=2, d_c=+2)]


if __name__ == '__main__':
    print(Cell.EMPTY.is_white == False)
    print(Cell.EMPTY.is_black == False)

    print(Cell.WHITE.is_black == False)
    print(Cell.WHITE.is_white == True)

    print(Cell.BLACK.is_black == True)
    print(Cell.BLACK.is_white == False)

    print(Cell.K_WHITE.is_black == False)
    print(Cell.K_WHITE.is_white == True)

    print(Cell.K_BLACK.is_black == True)
    print(Cell.K_BLACK.is_white == False)

    print(Cell.BLACK.same_color(Cell.K_BLACK))
    print(Cell.WHITE.same_color(Cell.K_BLACK))
    print(Cell.EMPTY.same_color(Cell.K_WHITE))
    print(Cell.WHITE.same_color(Cell.EMPTY))
