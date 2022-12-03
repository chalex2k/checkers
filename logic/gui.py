import random
from tkinter import *

from board import Board
from cell import Cell
from coord import Coord

# import tkMessageBox

root = Tk()


f = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]


board = Board()
cell_symbols = {
        Cell.EMPTY: ' ',
        Cell.WHITE: ' O ',
        Cell.K_WHITE: ' W ',
        Cell.BLACK: ' # ',
        Cell.K_BLACK: ' B ',
    }

def update_f():
    for r in range(len(board.field)):
        for c in range(len(board.field[r])):
            f[r][c].delete(0, END)
            f[r][c].insert(0, cell_symbols[board.field[r][c]])




c1: Entry = None
c2: Entry = None



def helloCallBack():
    user(*map(int, c1.get().split()))
    computer()
    update_f()



def init_grid():
    global c1
    global c2
    height = 9
    width = 9
    for i in range(height): #Rows
        for j in range(width): #Columns
            if i == 0 and j == 0:
                text = ''
            elif i == 0:
                text = str(j-1)
            elif j == 0:
                text = str(i-1)
            else:
                text = ''

            if i * j == 0:
                color = 'white'
            elif (i + j) % 2:
                color = 'gray'
            else:
                color = 'white'

            b = Entry(root, width = 3, background=color, borderwidth=0, font=50,)
            b.insert(0, text)
            b.grid(row=i, column=j)
            if 0 < i < 9 and 0 < i < 9:
                f[i-1][j-1] = b

    w = Button(root, text ="OK", command = helloCallBack)
    w.grid(row=9, column=0)

    c1 = Entry(root, width=6, background='white', borderwidth=0, font=50,)
    c1.grid(row=9, column=1, columnspan=4)
    # c2 = Entry(root, width=6, background='blue', borderwidth=0, font=50,)
    # c2.grid(row=9, column=3, columnspan=2)


init_grid()


INF = 1e6


def negamax(depth: int, color):
    score = -INF
    bests_moves = []
    if depth == 0:
        return evaluate(), None
    for move in board.variants(color):
        board.apply(move)
        tmp_score, _ = negamax(depth-1, Cell.BLACK if color == Cell.WHITE else Cell.WHITE)  # TODO OTHER COLOR
        tmp_score *= -1
        board.undo(move)
        if tmp_score > score:
            score = tmp_score
            bests_moves = [move]
        elif tmp_score == score:
            bests_moves.append(move)
    return score, random.choice(bests_moves)


def evaluate():
    return board.count(Cell.WHITE) + 3 * board.count(Cell.K_WHITE) \
           - board.count(Cell.BLACK) - 3 * board.count(Cell.K_BLACK)


def computer():
    _, best_move = negamax(2, Cell.BLACK)
    board.apply(best_move)


def user(fr, fc, tr, tc):
    # from_r, from_c = map(int, from_.split())
    # to_r, to_c = map(int, to.split())
    board.action(Coord(fr, fc), Coord(tr, tc))

update_f()

mainloop()
