import random

from logic.color import Color
from logic.exceptions import ComputerLostException

INF = 1e6


class Algorithm:
    def __init__(self, depth, algo):
        self.depth = depth
        self.algo = algo
        self.log = []

    def negamax(self, board, depth: int, color):
        score = -INF
        bests_moves = []
        if depth == 0:
            res = self.algo(board, color)
            self.log.append(f'score:{res} ')
            return res, None
        for move in board.variants(color):
            board.apply(move)
            self.log.append(str(move))
            tmp_score, _ = self.negamax(board, depth-1, Color.BLACK if color == Color.WHITE else Color.WHITE)
            tmp_score *= -1
            board.undo()
            if tmp_score > score:
                score = tmp_score
                bests_moves = [move]
            elif tmp_score == score:
                bests_moves.append(move)
        if bests_moves:
            return score, random.choice(bests_moves)
        return -INF, None

    def calculate_step(self, board):
        self.log.clear()
        _, best_move = self.negamax(board, self.depth, Color.BLACK)
        if best_move is None:
            raise ComputerLostException()
        board.apply(best_move)


class AlgorithmAlfaBeta:
    def __init__(self, depth, algo):
        self.depth = depth
        self.algo = algo
        self.log = []

    def negamax_alfa_beta(self, board, depth: int, color, maxW, maxB):
        score = -INF
        bests_moves = []
        if depth == 0:
            res = self.algo(board, color)
            self.log.append(f'score:{res} ')
            return res, None
        for move in board.variants(color):
            board.apply(move)
            self.log.append(str(move))
            tmp_score, _ = self.negamax_alfa_beta(board, depth-1,
                                                  Color.BLACK if color == Color.WHITE else Color.WHITE, maxW, maxB)
            tmp_score *= -1
            board.undo()
            if tmp_score > score:
                score = tmp_score
                bests_moves = [move]
                if color == Color.WHITE:
                    if score > maxW:
                        maxW = score
                    if -maxW  <= maxB:
                        return maxW, move
                else:
                    if score > maxB:
                        maxB = score
                    if -maxB <= maxW:
                        return maxB, move
            elif tmp_score == score:
                bests_moves.append(move)
        if bests_moves:
            return score, random.choice(bests_moves)
        return -INF, None

    def calculate_step(self, board):
        self.log.clear()
        _, best_move = self.negamax_alfa_beta(board, self.depth, Color.BLACK, -INF, -INF)
        if best_move is None:
            raise ComputerLostException()
        board.apply(best_move)