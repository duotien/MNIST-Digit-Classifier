import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('ui/fMain.ui', self)
        self.show()
        '''Find Children'''
        #layouts
        # self.layout_: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'layout_')
        self.hlayout_buttons: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'hlayout_buttons')
        self.vlayout_canvas: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'vlayout_canvas')

        # labels
        # self.lbl_: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_')
        self.lbl_canvas: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_canvas')
        # buttons
        # self.btn_: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_') #use this for template
        self.btn_open: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_open')
        self.btn_clear: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_clear')
        self.btn_detect: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_detect')
        # self.menuFile = self.findChild(QtWidgets.)
        # self.menuABout = self.findChild(QtWidgets.)

        # actions
        self.actionOpen: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionOpen')
        self.actionExit: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionExit')
        self.actionNew: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionNew')
        '''end findChildren'''
        '''connection'''
        # is_clicked
        # self.btn_.clicked.connect(lambda: self.isClicked('btn_'))
        self.btn_open.clicked.connect(lambda: self.isClicked('open'))
        self.btn_clear.clicked.connect(lambda: self.isClicked('clear'))
        self.btn_detect.clicked.connect(lambda: self.isClicked('detect'))

        # buttons
        # self.btn_apply.clicked.connect(self.test_combobox)
        self.btn_open.clicked.connect(self.openFile)
        self.btn_clear.clicked.connect(self.clearCanvas)
        # actions
        self.actionOpen.triggered.connect(self.openFile)
        self.actionNew.triggered.connect(self.newCanvas)
        '''end connection'''
        '''preloaded'''
        self.original_image = None
        self.image = None
        self.path = ''
        self.default_width = self.lbl_canvas.width()-4
        self.default_height = self.lbl_canvas.height()-8
        print(self.default_width, self.default_height)

    def isClicked(self, obj: str):
        '''
        Check if the object is clicked, result is printed in the console
        :param obj: the name of the object, in string
        :return: None
        '''
        print("{} was clicked".format(obj))
        print(self.lbl_canvas.size().width())

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', 'Image files (*.png *.xpm *.jpg *.tif)')
        # print(filename)
        if filename[0] != '' and filename[0] != None:
            self.path = filename[0]
            self.original_image = cv2.imread(filename[0])
            self.image = self.original_image
            self.showImage(self.lbl_canvas, self.image)
        else:
            print("invalid file")

    def showImage(self, label: QtWidgets.QLabel, cv_img=None):
        if cv_img is None:
            cv_img = self.image
        if cv_img is not None:
            height, width = cv_img.shape[:2]
            bytes_per_line = 3 * width
            q_img = QtGui.QImage(cv_img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
            label.setPixmap(QtGui.QPixmap(q_img))
        else:
            print("Warning: self.image is empty.")

    def newCanvas(self):
        canvas = self.createCanvas()
        self.lbl_canvas.setPixmap(canvas)

    def clearCanvas(self):
        width = self.lbl_canvas.width()-4
        height = self.lbl_canvas.height()-4
        canvas = self.createCanvas(width, height)
        self.lbl_canvas.setPixmap(canvas)

    def createCanvas(self, width: int = None, height: int = None, color = '#ffffff'):
        if width is None: width = self.default_width
        if height is None: height = self.default_height
        canvas = QtGui.QPixmap(width, height)
        canvas.fill(QtGui.QColor(color))
        return canvas

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tmp = Ui_MainWindow()
    app.exec_()
