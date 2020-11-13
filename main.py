import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('ui/fMain.ui', self)
        '''preloaded'''
        self.original_image = None
        self.image = None
        self.path = ''

        '''Find Children'''
        # labels
        # self.lbl_: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_')

        # buttons
        # self.btn_: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_') #use this for template

        # self.menuFile = self.findChild(QtWidgets.)
        # self.menuABout = self.findChild(QtWidgets.)

        # actions
        self.actionOpen: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionOpen')
        self.actionExit: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionExit')
        '''end findChildren'''
        '''connection'''
        # is_clicked
        # self.btn_apply.clicked.connect(lambda: self.isClicked('btn_apply'))

        # buttons
        # self.btn_apply.clicked.connect(self.test_combobox)

        # actions
        self.actionOpen.triggered.connect(self.openFile)
        '''end connection'''

        self.show()

    def isClicked(self, obj: str):
        '''
        Check if the object is clicked, result is printed in the console
        :param obj: the name of the object, in string
        :return: None
        '''
        print("{} was clicked".format(obj))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tmp = Ui_MainWindow()
    app.exec_()
