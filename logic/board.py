from copy import deepcopy
from typing import Union

from logic.jump import Jump, Take
from logic.exceptions import InvalidActionException
from logic.cell import Cell as cl, Cell
from logic.color import Color as C, Color
from logic.coord import Coord
from logic.move import Move
from logic.move_direction import MoveDirection

UC_WHITE = 0
UC_BLACK = 1


def opposites(cell: cl):
    if cell in (cl.BLACK, cl.K_BLACK):
        return [cl.WHITE, cl.K_WHITE]
    elif cell in (cl.WHITE, cl.K_WHITE):
        return [cl.BLACK, cl.K_BLACK]
    raise ValueError


def sames(cell: cl):
    if cell in (cl.BLACK, cl.K_BLACK):
        return [cl.BLACK, cl.K_BLACK]
    elif cell in (cl.WHITE, cl.K_WHITE):
        return [cl.WHITE, cl.K_WHITE]
    raise ValueError


def on_one_diagonal(from_: Coord, to: Coord):
    return from_.r - to.r == from_.c - to.c or from_.r + from_.c == to.r + to.c


class Board:
    def placement(self) -> list[list[int]]:
        """
        Расположение фигур на доске:
        0 - пустая клетка
        1 - белая шашка
        -1 - чёрная шашка
        2 - белая дамка
        -2 - чёрная дамка
        """
        return [[c.value for c in row] for row in self.field]

    def __init__(self, user_color='white'):
        self.user_color = UC_WHITE if user_color == 'white' else UC_BLACK
        # start placement
        # Белые внизу !
        self.field: list[list[Cell]] = [
            [Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK],
            [Cell.BLACK, Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK, Cell.EMPTY],
            [Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK, Cell.EMPTY, Cell.BLACK],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY],
            [Cell.EMPTY, Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY, Cell.WHITE],
            [Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY, Cell.WHITE, Cell.EMPTY],
        ]
        self.history: list[Union[Move, Take]] = []

    def action(self, path: list[Coord]):
        """
        Совершает ход - перемещение или взятие по координатам, если это возможно. Иначе InvalidActionException.
        """
        if len(path) < 2:
            raise InvalidActionException
        start = self.get(path[0])
        before = deepcopy(self.field)
        if start.is_checker:
            for direction in start.directions_moves:
                if path[1] == direction.apply(path[0]):
                    if len(path) == 2:
                        self.apply(Move(start, path[0], path[1], deepcopy(before)))
                        return
            jumps = []
            for i in range(1, len(path)):
                for direction in start.directions_takes:
                    if path[i] == direction.apply(path[i - 1]):
                        jumps.append(Jump(path[i - 1], path[i]))
                        break
                else:
                    raise InvalidActionException
            self.apply(Take(start, jumps, deepcopy(before)))
            return
        elif start.is_queen:
            jumps = []
            first = path[0]
            for i in range(len(path)-1):
                from_ = path[i]
                to = path[i + 1]
                if on_one_diagonal(from_, to) and self.get(to) == Cell.EMPTY:
                    if self._is_diagonal_empty(from_, to):
                        self.apply(Move(self.get(from_), from_, to, deepcopy(before)))
                        return
                    elif self.count_on_diagonal(opposites(self.get(first)), from_, to) == 1 and \
                            self.count_on_diagonal(sames(self.get(first)), from_, to) == 0:
                        jumps.append(Jump(from_, to))
                else:
                    raise InvalidActionException
            self.apply(Take(start, jumps, deepcopy(before)))
        else:
            raise InvalidActionException

    def apply(self, x: Union[Move, Take]):
        if isinstance(x, Move):
            self.apply_move(x)
            self.history.append(x)
            return
        elif isinstance(x, Take):
            self.take(x)
            self.history.append(x)
            return
        raise ValueError

    def undo(self):
        x = self.history.pop()
        if isinstance(x, Move):
            return self.undo_move(x)
        elif isinstance(x, Take):
            return self.undo_take(x)
        raise ValueError

    def get(self, coord: Coord) -> Cell:
        return self.field[coord.r][coord.c]

    def set(self, coord: Coord, f: Cell):
        if f == Cell.BLACK and coord.r == len(self.field) - 1:
            self.field[coord.r][coord.c] = Cell.K_BLACK
        elif f == Cell.WHITE and coord.r == 0:
            self.field[coord.r][coord.c] = Cell.K_WHITE
        else:
            self.field[coord.r][coord.c] = f

    def variants(self, color=Color.BLACK):
        if takes := list(self.takes_variants(color)):
            return takes
        else:
            return self.moves_variants(color)

    def is_color(self, coord: Coord, color: C):
        if color == color.WHITE:
            return self.get(coord).is_white
        return self.get(coord).is_black

    def foreach(self, color: Color):
        for r in range(len(self.field)):
            for c in range(len(self.field[r])):
                coord = Coord(r, c)
                if self.is_color(coord, color):
                    yield coord, self.get(coord)

    def _is_valid(self, r, c):
        return 0 <= r < len(self.field) and 0 <= c < len(self.field[0])

    def _is_empty(self, c: Coord):
        return self._is_valid(c.r, c.c) and self.field[c.r][c.c] == Cell.EMPTY

    def moves_variants(self, color=Color.BLACK) -> list[Move]:
        moves = []
        before = deepcopy(self.field)
        for coord, cell in self.foreach(color):
            if cell.is_checker:
                for direction in cell.directions_moves:
                    if self._is_empty(direction.apply(coord)):
                        moves.append(Move(cell, coord, direction.apply(coord), deepcopy(before)))
            elif cell.is_queen:
                for direction in cell.directions_moves:
                    next_coord = direction.apply(coord)
                    while self._is_empty(next_coord):
                        moves.append(Move(cell, coord, next_coord, deepcopy(before)))
                        next_coord = direction.apply(next_coord)
        return moves

    def apply_move(self, move: Move):
        if self.get(move.from_) == Cell.EMPTY or self.get(move.to) != Cell.EMPTY:
            raise ValueError
        self.set(move.to, self.get(move.from_))
        self.set(move.from_, Cell.EMPTY)

    def undo_move(self, move: Move):
        self.field = move.field_before

    def takes_variants(self, color=Color.BLACK):
        takes = []
        before = deepcopy(self.field)
        for coord, f in self.foreach(color):
            if f.is_checker:
                for move_dir in f.directions_takes:
                    coord1 = move_dir.apply(coord)
                    candidate1 = Jump(coord, coord1)
                    if self._is_empty(move_dir.apply(coord)) and self.is_color(move_dir.taken(coord),
                                                                                self.opposite(color)):
                        flg = False
                        for direction2 in f.directions_takes:
                            if move_dir + direction2 == 0:
                                continue
                            candidate2 = Jump(coord1, direction2.apply(coord1))
                            if self._is_empty(direction2.apply(coord1)) and self.is_color(direction2.taken(coord1),
                                                                                         self.opposite(color)):
                                takes.append(
                                    Take(f, [candidate1, candidate2], deepcopy(before))
                                )
                                flg = True
                        if not flg:
                            takes.append(Take(f, [candidate1], deepcopy(before)))
            elif f.is_queen:
                for move_dir in [MoveDirection(d_r=-1, d_c=-1), MoveDirection(d_r=-1, d_c=+1),
                                           MoveDirection(d_r=+1, d_c=-1), MoveDirection(d_r=+1, d_c=+1)]:
                    coord1 = move_dir.apply(coord)
                    while self._is_empty(coord1):
                        coord1 = move_dir.apply(coord1)
                    if self._is_valid(coord1.r, coord1.c) and self.is_color(coord1, self.opposite(color)):
                        coord1 = move_dir.apply(coord1)
                        while self._is_empty(coord1):
                            candidate1 = Jump(coord, coord1)
                            flg = False
                            for direction2 in [MoveDirection(d_r=-1, d_c=-1), MoveDirection(d_r=-1, d_c=+1),
                                               MoveDirection(d_r=+1, d_c=-1), MoveDirection(d_r=+1, d_c=+1)]:
                                if move_dir + direction2 == 0:
                                    continue
                                coord2 = move_dir.apply(coord1)
                                while self._is_empty(coord2):
                                    coord2 = move_dir.apply(coord2)
                                if self._is_valid(coord2.r, coord2.c) and self.is_color(coord2, self.opposite(color)):
                                    coord2 = move_dir.apply(coord2)
                                    while self._is_empty(coord2):
                                        candidate2 = Jump(coord1, coord2)
                                        takes.append(
                                            Take(f, [candidate1, candidate2], deepcopy(before))
                                        )
                                        flg = True
                            if not flg:
                                takes.append(Take(f, [candidate1], deepcopy(before)))
                            coord1 = move_dir.apply(coord1)
        return takes

    def take(self, t: Take):
        for j in t.jumps:
            self.set(j.to, self.get(j.from_))
            self.set(j.from_, Cell.EMPTY)
            for coord in j.taken_coord:
                self.set(coord, Cell.EMPTY)

    def undo_take(self, t: Take):
        self.field = t.field_before

    def count(self, color: Color):
        cnt = 0
        for r in range(len(self.field)):
            for c in range(len(self.field[r])):
                if self.is_color(Coord(r, c), color):
                    cnt += 1
        return cnt

    @staticmethod
    def opposite(color: Color):
        if color == Color.WHITE:
            return Color.BLACK
        elif color == Color.BLACK:
            return Color.WHITE
        raise ValueError

    def _is_diagonal_empty(self, from_: Coord, to: Coord):
        for r, c, i in zip(
                range(from_.r, to.r, (to.r - from_.r) // abs(to.r - from_.r) ),
                range(from_.c, to.c, (to.c - from_.c) // abs(to.c - from_.c) ),
                range(abs(to.r - from_.r))
        ):
            if i == 0:
                continue
            if self.get(Coord(r, c)) != cl.EMPTY:
                return False
        return True

    def count_on_diagonal(self, types, from_: Coord, to: Coord):
        cnt = 0
        for r, c, i in zip(
                range(from_.r, to.r, (to.r - from_.r) // abs(to.r - from_.r) ),
                range(from_.c, to.c, (to.c - from_.c) // abs(to.c - from_.c)),
                range(abs(to.r - from_.r))
        ):
            if i == 0:
                continue
            if self.get(Coord(r, c)) in types:
                cnt += 1
        return cnt

    def allow_user_move(self, c: Coord):
        if self.user_color == UC_WHITE:
            return self.is_color(c, C.WHITE)
