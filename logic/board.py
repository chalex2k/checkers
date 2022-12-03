from typing import Union

from .Take import Take
from .cell import Cell as cl
from .color import Color as C
from .coord import Coord
from .move import Move
from .move_direction import MoveDirection
from .take_direction import TakeDirection
from .figures import *

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
    return from_.r - to.r == from_.c - to.c or from_.r + to.r == from_.c + to.c


class Board:
    _cell_symbols = {
        cl.EMPTY: '   ',
        cl.WHITE: ' O ',
        cl.K_WHITE: ' W ',
        cl.BLACK: ' # ',
        cl.K_BLACK: ' B ',
    }

    def __init__(self, user_color = 'white'):
        self.user_color = UC_WHITE if user_color == 'white' else UC_BLACK
        # start placement
        # Белые внизу !
        self.field: list[list[Figure]] = [
            [Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK)],
            [Checker(C.BLACK), Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK), Empty()],
            [Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK), Empty(), Checker(C.BLACK)],
            [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
            [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
            [Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty()],
            [Empty(), Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty(), Checker(C.WHITE)],
            [Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty(), Checker(C.WHITE), Empty()],
        ]

    def __str__(self):
        numbers = '   '+' | '.join(str(i) for i in range(8))
        horisontal = ' ├---' + '┼---' * 6 + '┼---┤'
        lines: list[str] = [numbers, horisontal]
        nrow = 0
        for row in self.field:
            line = str(nrow) + '|'
            nrow += 1
            for cell in row:
                line += self._cell_symbols[cell]
                line += '|'
            lines.append(line)
            lines.append(horisontal)
        return '\n'.join(lines)

    def get(self, coord: Coord):
        return self.field[coord.r][coord.c]

    def set(self, coord: Coord, f: Figure):
        self.field[coord.r][coord.c] = f

    def variants(self, color=Color.BLACK):
        if takes := list(self.takes_variants(color)):
            return takes
        else:
            return self.moves_variants(color)


    def is_color(self, coord: Coord, color: C):
        f = self.get(coord)
        return isinstance(f, (Checker, Queen)) and f.color == color

    def foreach(self, color: Color):
        for r in range(len(self.field)):
            for c in range(len(self.field[r])):
                coord = Coord(r, c)
                if self.is_color(coord, color):
                    yield coord, self.get(coord)

    def _is_valid(self, r, c):
        return 0 <= r < len(self.field) and 0 <= c < len(self.field[0])

    def _is_empty(self, c: Coord):
        return self._is_valid(c.r, c.c) and isinstance(self.field[c.r][c.c], Empty)

    def moves_variants(self, color=Color.BLACK):
        moves = []
        for coord, f in self.foreach(color):
            for direction in f.directions_moves:
                candidate = Move(f, coord, direction.apply(coord))
                if self._is_empty(direction.apply(coord)):
                    moves.append(candidate)
        return moves

    def apply(self, x: Union[Move, Take]):
        if isinstance(x, Move):
            return self.apply_move(x)
        elif isinstance(x, Take):
            return self.take(x)
        raise ValueError

    def undo(self, x: Union[Move, Take]):
        if isinstance(x, Move):
            return self.undo_move(x)
        elif isinstance(x, Take):
            return self.undo_take(x)
        raise ValueError

    def apply_move(self, move: Move):
        if not isinstance(self.get(move.from_), Figure) or not isinstance(self.get(move.to), Empty):
            raise ValueError
        self.set(move.to, self.get(move.from_))
        self.set(move.from_, Empty())

    def undo_move(self, move: Move):
        if not (self.get(move.to) == move.checker and isinstance(self.get(move.from_), Empty)):
            raise ValueError
        self.set(move.from_, self.get(move.to))
        self.set(move.to, Empty)



    def get_chains(self, take: Take) -> list[list[Take]]:
        self.take(take)

    def check_take(self, r, c):
        pass

    def takes_variants(self, color = Color.BLACK):
        take_chains = []
        for coord, f in self.foreach(color):
            for direction in f.directions_takes:
                coord1 = direction.apply(coord)
                candidate1 = Take(f, coord, coord1)
                if self._is_empty(direction.apply(coord)) and self.is_color(direction.taken(coord), self.opposite(color)):
                    flg = False
                    for direction2 in f.directions_takes:
                        if direction + direction2 == 0:
                            continue
                        candidate2 = Take(f, coord1, direction.apply(coord1))
                        if self._is_empty(direction.apply(coord1)) and self.is_color(direction.taken(coord1), self.opposite(color)):
                            take_chains.append(
                                [candidate1, candidate2]
                            )
                            flg = True
                    if not flg:
                        take_chains.append([candidate1])
        return take_chains

    def take(self, t: Take):
        if not (self.get(t.from_) == t.checker and self.get(t.to) == cl.EMPTY and self.get(t.taken_coord) == self.opposite(t.checker)):
            raise ValueError
        # TODO Если это дамка, то нужно запоминать где стояла
        # Нужно запоминать кто тут стоял was_taken
        self.set(t.to, self.get(t.from_))
        self.set(t.from_, cl.EMPTY)
        self.set(t.taken_coord, cl.EMPTY)

    def undo_take(self, t: Take):
        # todo check
        self.set(t.from_, self.get(t.to))
        self.set(t.to, cl.EMPTY)
        self.set(t.taken_coord, self.opposite(t.checker))


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

    def action(self, move: list[Coord]):
        """
        Совершает ход - перемещение или взятие по координатам, если это возможно. Иначе ValueError.
        """
        if len(move) < 2:
            raise ValueError
        start = self.get(move[0])
        if isinstance(start, Checker):
            for direction in start.directions_moves:
                if move[1] == direction.apply(move[0]):
                    if len(move) == 2:
                        return self.apply(Move(start, move[0], move[1]))
            for i in range(1, len(move)):
                moves = []
                for direction in start.directions_takes:
                    if move[i] == direction.apply(move[i-1]):
                        moves.append(self.apply(Take(start, move[i-1], move[i])))
                        break
                else:
                    raise ValueError
                return moves
        elif isinstance(start, Queen):
            if on_one_diagonal(from_, to):
                if self.is_diagonal_empty(from_, to):
                    self.apply(Move(self.get(from_), from_, to))
                    return
                elif self.count_on_diagonal(opposites(self.get(from_)), from_, to) == 1 and \
                        self.count_on_diagonal(sames(self.get(from_)), from_, to) == 0:
                    self.apply(Take(self.get(from_), from_, to))
                    return
        else:
            raise ValueError

    def is_diagonal_empty(self, from_: Coord, to: Coord):
        for r, c in zip(range(min(from_.r, to.r), max(from_.r, to.r)), range(min(from_.c, to.c), max(from_.c, to.c))):
            if self.get(Coord(r, c)) != cl.EMPTY:
                return False
        return True

    def count_on_diagonal(self, types, from_: Coord, to: Coord):
        cnt = 0
        for r, c in zip(range(min(from_.r, to.r), max(from_.r, to.r)), range(min(from_.c, to.c), max(from_.c, to.c))):
            if self.get(Coord(r, c)) in types:
                cnt += 1
        return cnt



    def allow_user_move(self, c: Coord):
        if self.user_color == UC_WHITE:
            return self.is_color(c, C.WHITE)

    # def computer(self):
    #     _, best_move = negamax(2, Cell.BLACK)
    #     board.apply(best_move)
