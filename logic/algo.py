import random

from logic.cell import Cell
from logic.color import Color

INF = 1e6


class Algorithm:
    def __init__(self, depth):
        self.depth = depth

    @staticmethod
    def negamax(board, depth: int, color):
        score = -INF
        bests_moves = []
        if depth == 0:
            return Algorithm.evaluate(board, color), None
        for move in board.variants(color):
            board.apply(move)
            tmp_score, _ = Algorithm.negamax(board, depth-1, Color.BLACK if color == Color.WHITE else Color.WHITE)  # TODO OTHER COLOR
            tmp_score *= -1
            board.undo()
            if tmp_score > score:
                score = tmp_score
                bests_moves = [move]
            elif tmp_score == score:
                bests_moves.append(move)
        return score, random.choice(bests_moves)

    @staticmethod
    def evaluate(board, color):
        if color == Color.WHITE:
            return board.count(Color.WHITE) + 3 * board.count(Color.WHITE) \
                   - board.count(Color.BLACK) - 3 * board.count(Color.BLACK)
        else:
            return board.count(Color.BLACK) + 3 * board.count(Color.BLACK) \
                - board.count(Color.WHITE) - 3 * board.count(Color.WHITE)

    def computer(self, board):
        _, best_move = self.negamax(board, self.depth, Color.BLACK)
        board.apply(best_move)
