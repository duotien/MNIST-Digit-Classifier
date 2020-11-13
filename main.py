import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(600, 300)
        # pixmap = QtGui.QPixmap(self.width(), self.height())
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        pixmap.fill(QtGui.QColor('#ffffff'))
        self.setPixmap(pixmap)
        self.pen_color = QtGui.QColor('#000000')
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumSize(10, 10)
        self.last_x, self.last_y = None, None

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        self.update()

    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap(600, 300)
        # pixmap = QtGui.QPixmap(self.width(),self.height())
        pixmap.fill(QtGui.QColor('#ffffff'))
        pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('ui/fMain.ui', self)
        self.show()
        '''Find Children'''
        # layouts
        # self.layout_: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'layout_')
        self.hlayout_buttons: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'hlayout_buttons')
        self.vlayout_canvas: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'vlayout_canvas')
        self.scrollArea: QtWidgets.QScrollArea = self.findChild(QtWidgets.QScrollArea, 'scrollArea')
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
        self.actionSave: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionSave')
        '''end findChildren'''
        '''preloaded'''
        self.init_connection()
        self.init_variable()

    def init_variable(self):
        self.image = None
        self.cv_image = None
        self.path = ''
        self.default_width = self.lbl_canvas.width() - 4
        self.default_height = self.lbl_canvas.height() - 8
        self.last_x, self.last_y = None, None

        self.is_drawing = False
        self.pen_size = 4
        self.pen_color = QtCore.Qt.black

    def init_connection(self):
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
        self.actionSave.triggered.connect(self.saveImage)

    def isClicked(self, obj: str):
        '''
		Check if the object is clicked, result is printed in the console
		:param obj: the name of the object, in string
		:return: None
		'''
        print("{} was clicked".format(obj))

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', 'Image files (*.png *.xpm *.jpg *.tif)')
        # print(filename)
        if filename[0] != '' and filename[0] != None:
            self.path = filename[0]
            self.cv_image = cv2.imread(filename[0])
            self.showImage(self.lbl_canvas, self.cv_image)
        else:
            print("invalid file")

    def showImage(self, label: QtWidgets.QLabel, cv_img=None):
        if cv_img is None:
            cv_img = self.cv_image
        if cv_img is not None:
            height, width = cv_img.shape[:2]
            bytes_per_line = 3 * width
            self.image = QtGui.QImage(cv_img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
            label.setPixmap(QtGui.QPixmap(self.image))
        else:
            print("Warning: self.cv_image is empty.")

    def saveImage(self):
        if self.image is not None:
            filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "untitled.png",
                                                      "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

            if filePath == "":
                return
            self.image.save(filePath)

    def newCanvas(self):
        self.image = self.createCanvas()
        self.lbl_canvas.setPixmap(self.image)

    def clearCanvas(self):
        width = self.lbl_canvas.width() - 4
        height = self.lbl_canvas.height() - 4
        self.image = self.createCanvas(width, height)
        self.lbl_canvas.setPixmap(self.image)

    def createCanvas(self, width: int = None, height: int = None, color='#ffffff'):
        if width is None: width = self.default_width
        if height is None: height = self.default_height
        canvas = QtGui.QPixmap(width, height)
        canvas.fill(QtGui.QColor(color))
        return canvas

    def mousePressEvent(self, e):
        # if left mouse button is pressed
        if e.button() == QtCore.Qt.LeftButton:
            # make drawing flag true
            self.is_drawing = True
            self.last_x, self.last_y = e.x(), e.y()
            #print(self.last_x, self.last_y, self.is_drawing)

    def mouseMoveEvent(self, e):
        if self.lbl_canvas.pixmap() is not None and self.is_drawing:
            if self.last_x is None:  # First event.
                self.last_x = e.x()
                self.last_y = e.y()
                return  # Ignore the first time.

            #get lbl_canvas position -> QPoint(x,y)
            lbl_canvas_pos = self.lbl_canvas.mapTo(self, QtCore.QPoint(0, 0))

            painter = QtGui.QPainter(self.lbl_canvas.pixmap())
            painter.setWindow(lbl_canvas_pos.x(), lbl_canvas_pos.y(), self.lbl_canvas.pixmap().width(), self.lbl_canvas.pixmap().height())
            p = painter.pen()
            p.setWidth(self.pen_size)
            p.setColor(self.pen_color)
            painter.setPen(p)
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.lbl_canvas.update()
            self.image = self.lbl_canvas.pixmap()


            # Update the origin for next time.
            self.last_x = e.x()
            self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.last_x = None
            self.last_y = None
            self.is_drawing = False
            #print(self.last_x, self.last_y, self.is_drawing)

    def paintEvent(self, event):
        if self.lbl_canvas.pixmap() is not None:
            width = self.lbl_canvas.width()
            height = self.lbl_canvas.height()
            self.lbl_canvas.pixmap().scaled(width, height)
            #print("paint")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tmp = Ui_MainWindow()
    #canvas = Canvas()
    #canvas.show()
    app.exec_()
