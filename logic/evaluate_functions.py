from logic.board import Board
from logic.color import Color

"""
Функции оценки состояния
"""


def evaluate(board: Board, color: Color):
    """
    Дамка равна 3 шашкам
    """
    if color == Color.WHITE:
        score = 0
        for r in range(len(board.field)):
            for c in range(len(board.field[0])):
                if board.field[r][c].is_white:
                    if board.field[r][c].is_checker:
                        score += 1
                    elif board.field[r][c].is_queen:
                        score += 3
                    else:
                        raise ValueError
                elif board.field[r][c].is_black:
                    if board.field[r][c].is_checker:
                        score -= 1
                    elif board.field[r][c].is_queen:
                        score -= 3
                    else:
                        raise ValueError
        return score
    else:
        score = 0
        for r in range(len(board.field)):
            for c in range(len(board.field[0])):
                if board.field[r][c].is_black:
                    if board.field[r][c].is_checker:
                        score += 1
                    elif board.field[r][c].is_queen:
                        score += 3
                    else:
                        raise ValueError
                elif board.field[r][c].is_white:
                    if board.field[r][c].is_checker:
                        score -= 1
                    elif board.field[r][c].is_queen:
                        score -= 3
                    else:
                        raise ValueError
        return score


def evaluate_position(board: Board, color: Color):
    """
    1. Нахождение шашек на бортовых полях снижает их боевыую эффективность
    2. Положение группы шашек в центре должно привести к инициативе, особенно полей с5, f4 - очень удобно препятствовать развитию сил противника
    """
    white_wethts = [
        [0, 3, 0, 5, 0, 5, 0, 3],
        [3, 0, 5, 0, 5, 0, 4, 0],
        [0, 3, 0, 4, 0, 4, 0, 3],
        [2, 0, 4, 0, 4, 0, 2, 0],
        [0, 2, 0, 3, 0, 4, 0, 2],
        [1, 0, 2, 0, 2, 0, 2, 0],
        [0, 1, 0, 2, 0, 2, 0, 1],
        [1, 0, 2, 0, 2, 0, 2, 0],
    ]

    if color == Color.WHITE:
        for r in range(len(board.field)):
            for c in range(len(board.field[0])):
                if board.field[r][c].is_white:  # и это только для шашек наверное
                    pass

