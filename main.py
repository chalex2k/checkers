import sys
from time import sleep

from first import *
from functools import partial

from logic.algo import Algorithm
from logic.board import Board
from logic.color import Color
from logic.coord import Coord
from logic.cell import Cell as cl
from logic.figures import Checker, Queen

BOARD_SIZE = 8

class Interface:
    def __init__(self):
        self.algo = Algorithm(1)
        self.board = Board()
        self.move = []
        self.ctrl_is_pressing = False
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.init_board_labels()
        self.draw_board()
        self.ui.pushButton.mousePressEvent = self.press_button
        self.ui.centralwidget.keyPressEvent = self.on_key_press
        self.ui.centralwidget.keyReleaseEvent = self.on_key_release
        MainWindow.show()
        sys.exit(app.exec())

    def on_key_press(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control.value:
            print("PRESS CTRL")
            self.ctrl_is_pressing = True
        event.accept()

    def on_key_release(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control.value:
            print("RELEASE CTRL")
            self.ctrl_is_pressing = False
        event.accept()

    def click_on_board(self, c: Coord, QMouseEvent):
        if not self.move:
            if self.board.allow_user_move(c):
                self.move.append(c)
        else:
            self.move.append(c)
            if not self.ctrl_is_pressing:
                self.board.action(self.move)
                self.move.clear()
                self.draw_board()
                sleep(0.5)
                self.algo.computer(self.board)
                self.draw_board()
        print(self.move)

    def init_board_labels(self):
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                label = QtWidgets.QLabel()
                label.mousePressEvent = partial(self.click_on_board, Coord(row, column))
                self.ui.gridLayoutBoard.addWidget(label, row, column)

    def draw_board(self):
        pixmap_black = QtGui.QPixmap('img/black_empty.png')
        pixmap_white = QtGui.QPixmap('img/white_empty.png')
        pixmap_white_checker = QtGui.QPixmap('img/white_checker.png')
        pixmap_black_checker = QtGui.QPixmap('img/black_checker.png')
        pixmap_white_queen = QtGui.QPixmap('img/white_queen.png')
        pixmap_black_queen = QtGui.QPixmap('img/black_queen.png')
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                label: QtWidgets.QLabel = self.ui.gridLayoutBoard.itemAtPosition(r, c).widget()
                pixmap = pixmap_black if (r + c) % 2 else pixmap_white
                if isinstance(self.board.field[r][c], Checker):
                    if self.board.field[r][c].color == Color.WHITE:
                        pixmap = pixmap_white_checker
                    else:
                        pixmap = pixmap_black_checker
                elif isinstance(self.board.field[r][c], Queen):
                    if self.board.field[r][c].color == Color.WHITE:
                        pixmap = pixmap_white_queen
                    else:
                        pixmap = pixmap_black_queen
                label.setPixmap(pixmap)

    def press_button(self, *args, **kwargs):
        print('press button', args, kwargs)
        new_position = [
            [0, 2, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 4, 0, 0, ],
            [0, 2, 0, 0, 0, 0, 1, 0, ],
            [0, 0, 2, 0, 0, 0, 0, 0, ],
            [0, 1, 0, 3, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, 0, 0, ],
            [1, 0, 0, 0, 0, 0, 0, 0, ],
        ]
        self.draw_board(new_position)


if __name__ == "__main__":
    Interface()



# from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication
#
# Form, Window = uic.loadUiType("first.ui")
#
# app = QApplication([])
# window = Window()
# form = Form()
# form.setupUi(window)
# window.show()
# app.exec()