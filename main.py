import sys
from time import sleep

from PyQt6.QtWidgets import QMessageBox

from first import *
from functools import partial
from logic.algorithm import Algorithm, AlgorithmAlfaBeta
from logic.board import Board
from logic.evaluate_functions import evaluate
from logic.exceptions import ComputerLostException
from logic.coord import Coord

BOARD_SIZE = 8


class Interface:
    def __init__(self):
        self.algorithm = Algorithm(1, evaluate)
        self.board = Board()
        self.move = []
        self.ctrl_is_pressing = False
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.pixmap_black = QtGui.QPixmap('img/black_empty.png')
        self.pixmap_white = QtGui.QPixmap('img/white_empty.png')
        self.pixmap_white_checker = QtGui.QPixmap('img/white_checker.png')
        self.pixmap_black_checker = QtGui.QPixmap('img/black_checker.png')
        self.pixmap_white_queen = QtGui.QPixmap('img/white_queen.png')
        self.pixmap_black_queen = QtGui.QPixmap('img/black_queen.png')

        self.init_board_labels()
        self.draw_board()
        self.ui.pushButton.mousePressEvent = self.press_button_cancel
        self.ui.pushButtonStart.mousePressEvent = self.press_button_start
        self.ui.centralwidget.keyPressEvent = self.on_key_press
        self.ui.centralwidget.keyReleaseEvent = self.on_key_release

        self.MainWindow.show()
        sys.exit(app.exec())

    def on_key_press(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control.value:
            self.ctrl_is_pressing = True
        event.accept()

    def on_key_release(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control.value:
            self.ctrl_is_pressing = False
        event.accept()

    def click_on_board(self, c: Coord, QMouseEvent):
        if not self.move:
            if self.board.allow_user_move(c):
                self.move.append(c)
        else:
            self.move.append(c)
            if not self.ctrl_is_pressing:
                try:
                    self.board.action(self.move)
                    print(self.move)
                except Exception as e:
                    dialog = QMessageBox(parent=self.MainWindow, text=str(e))
                    print(e)
                    dialog.setWindowTitle("Message Dialog")
                    ret = dialog.exec()  # Stores the return value for the button pressed
                    # raise e
                else:
                    self.draw_board()
                    sleep(0.5)
                    print('computer moved')
                    try:
                        self.algorithm.calculate_step(self.board)
                    except ComputerLostException as e:
                        dialog = QMessageBox(parent=self.MainWindow, text="Белые победили")
                        dialog.setWindowTitle("Конец игры")
                        ret = dialog.exec()  # Stores the return value for the button pressed
                    self.ui.plainTextEditLog.appendPlainText('\n' + '-'.join(self.algorithm.log))
                finally:
                    self.move.clear()
                    self.draw_board()

    def init_board_labels(self):
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                label = QtWidgets.QLabel()
                label.mousePressEvent = partial(self.click_on_board, Coord(row, column))
                self.ui.gridLayoutBoard.addWidget(label, row, column)

    def draw_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                label: QtWidgets.QLabel = self.ui.gridLayoutBoard.itemAtPosition(r, c).widget()
                pixmap = self.pixmap_black if (r + c) % 2 else self.pixmap_white
                if self.board.field[r][c].is_checker:
                    if self.board.field[r][c].is_white:
                        pixmap = self.pixmap_white_checker
                    else:
                        pixmap = self.pixmap_black_checker
                elif self.board.field[r][c].is_queen:
                    if self.board.field[r][c].is_white:
                        pixmap = self.pixmap_white_queen
                    else:
                        pixmap = self.pixmap_black_queen
                label.setPixmap(pixmap)

    def press_button_cancel(self, *args, **kwargs):
        self.board.undo()
        self.board.undo()
        self.draw_board()

    def press_button_start(self, *args, **kwargs):
        self.board = Board()
        self.move.clear()
        depth = 1
        if self.ui.comboBoxAlgo.currentIndex() == 1:
            depth = 2
        elif self.ui.comboBoxAlgo.currentIndex() == 2:
            depth = 3
        elif self.ui.comboBoxAlgo.currentIndex() == 3:
            depth = 4
        elif self.ui.comboBoxAlgo.currentIndex() == 4:
            depth = 5
        elif self.ui.comboBoxAlgo.currentIndex() == 5:
            depth = 6
        print(depth)
        # self.algorithm = AlgorithmAlfaBeta(depth, evaluate)
        self.algorithm = Algorithm(depth, evaluate)
        self.ui.plainTextEditLog.clear()
        self.draw_board()


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
