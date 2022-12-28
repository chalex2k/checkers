import random
from pprint import pprint

from Jump import Jump
from board import Board
from cell import Cell
from coord import Coord
from move import Move

board = Board()

INF = 1e6


def negamax(depth: int):
    score = -INF
    bests_moves = []
    if depth == 0:
        return evaluate()
    for move in board.variants():
        board.apply(move)
        tmp_score = -negamax(depth-1)  # TODO OTHER COLOR
        board.undo(move)
        if tmp_score > score:
            score = tmp_score
            bests_moves = [move]
        elif tmp_score == score:
            bests_moves.append(move)
    return random.choice(bests_moves)


def evaluate():
    return board.count(Cell.WHITE) + board.count(Cell.K_WHITE) - board.count(Cell.BLACK) - board.count(Cell.K_BLACK)


def computer():
    best_move = negamax(1)
    board.apply(best_move)


def user():
    from_r, from_c = map(int, input('from (r c) : ').split())
    to_r, to_c = map(int, input('to (r c) : ').split())
    board.action([Coord(from_r, from_c), Coord(to_r, to_c)])


def print_board():
    print()
    print(board)


def gameloop():
    while True:  # TODO is one win
        print_board()
        user()
        print_board()
        computer()


# gameloop()

# дамки и операции с ними
# оценочная функция материал шашек и дамок + какая-то позиция
#  1 дамка = 3 шашек, 2 шашки в центре чуть лучше чем 3 шашки на флангах
# логирование
# поэкспериментировать с глубиной



# альфа бета отсечение
# сортировка вариантов
# игрок и белыми и чёрными
# бить несколько. компьютер и игрок



