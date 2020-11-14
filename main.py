import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from tensorflow.keras import models

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
        # spinbox
        self.sbox_brush_size: QtWidgets.QSpinBox = self.findChild(QtWidgets.QSpinBox, 'sbox_brush_size')

        # actions
        self.actionOpen: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionOpen')
        self.actionExit: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionExit')
        self.actionNew: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionNew')
        self.actionSave: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionSave')
        '''end findChildren'''

        '''Connection'''
        # is_clicked
        # self.btn_.clicked.connect(lambda: self.isClicked('btn_'))
        self.btn_open.clicked.connect(lambda: self.isClicked('open'))
        self.btn_clear.clicked.connect(lambda: self.isClicked('clear'))
        self.btn_detect.clicked.connect(lambda: self.isClicked('detect'))

        # buttons
        # self.btn_apply.clicked.connect(self.test_combobox)
        self.btn_open.clicked.connect(self.openFile)
        self.btn_clear.clicked.connect(self.clearCanvas)
        self.btn_detect.clicked.connect(self.detect)

        # spinboxes
        self.sbox_brush_size.valueChanged.connect(self.changeBrushSize)

        # actions
        self.actionOpen.triggered.connect(self.openFile)
        self.actionNew.triggered.connect(self.newCanvas)
        self.actionSave.triggered.connect(self.saveImage)
        '''end Connection'''
        '''preloaded'''
        #self.init_connection()
        #self.init_variable()
        self.last_state_image = None
        self.backup_image = None
        self.cv_image = None
        self.path = ''
        self.default_width = self.lbl_canvas.width() - 4
        self.default_height = self.lbl_canvas.height() - 8
        self.last_x, self.last_y = None, None

        self.model = models.load_model('model/emnist_final.h5')

        self.is_detecting = False
        self.is_drawing = False
        self.pen_size = 4
        self.pen_color = QtCore.Qt.black

    def init_variable(self):
        self.backup_image = None
        self.cv_image = None
        self.path = ''
        self.default_width = self.lbl_canvas.width() - 4
        self.default_height = self.lbl_canvas.height() - 8
        self.last_x, self.last_y = None, None

        self.model = models.load_model('model/emnist_final.h5')

        self.is_detecting = False
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
        self.btn_detect.clicked.connect(self.detect)
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
            self.backup_image = QtGui.QPixmap(self.convertMatToQImage(self.cv_image))
            self.showImage(self.lbl_canvas, self.cv_image)
        else:
            print("invalid file")

    def showImage(self, label: QtWidgets.QLabel, cv_img=None):
        if cv_img is not None:
            image = self.convertMatToQImage(cv_img)
            image = QtGui.QPixmap(image)
            label.setPixmap(image)
        else:
            print("Warning: self.cv_image is empty.")

    def convertMatToQImage(self, mat: np.ndarray=None):
        if mat is not None:
            height, width = mat.shape[:2]
            bytes_per_line = 3 * width
            image = QtGui.QImage(mat.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
            return image

    def saveImage(self):
        if self.lbl_canvas.pixmap() is not None:
            filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "untitled.png",
                                                      "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

            if filePath == "":
                return
            self.lbl_canvas.pixmap().save(filePath)

    def newCanvas(self):
        self.backup_image = None
        self.cv_image = None
        self.path = ''
        self.is_detecting = False
        self.is_drawing = False
        self.btn_detect.setText("Detect")
        self.switchDrawingMode(True)
        self.backup_image = self.createCanvas()
        self.lbl_canvas.setPixmap(self.backup_image)

    def clearCanvas(self):
        if self.lbl_canvas.pixmap() is not None:
            # width = self.lbl_canvas.pixmap().width()
            # height = self.lbl_canvas.pixmap().height()
            # self.backup_image = self.createCanvas(width, height)
            self.lbl_canvas.setPixmap(self.backup_image)

    def createCanvas(self, width: int = None, height: int = None, color='#ffffff'):
        if width is None: width = self.default_width
        if height is None: height = self.default_height
        canvas = QtGui.QPixmap(width, height)
        canvas.fill(QtGui.QColor(color))
        return canvas

    def mousePressEvent(self, e):
        if self.lbl_canvas.pixmap() is not None:
            if e.button() == QtCore.Qt.LeftButton and not self.is_detecting:
                self.is_drawing = True

                self.last_x, self.last_y = e.x(), e.y()

                lbl_canvas_pos = self.lbl_canvas.mapTo(self, QtCore.QPoint(0, 0))

                painter = QtGui.QPainter(self.lbl_canvas.pixmap())
                painter.setWindow(lbl_canvas_pos.x(), lbl_canvas_pos.y(), self.lbl_canvas.pixmap().width(),
                                  self.lbl_canvas.pixmap().height())
                p = painter.pen()
                p.setWidth(self.pen_size)
                p.setColor(self.pen_color)
                painter.setPen(p)
                painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
                painter.end()
                self.lbl_canvas.update()
                #self.image = self.lbl_canvas.pixmap()

                print(self.last_x, self.last_y, self.is_drawing)

    def mouseMoveEvent(self, e):
        if self.lbl_canvas.pixmap() is not None and self.is_drawing and not self.is_detecting:
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
            #self.image = self.lbl_canvas.pixmap()

            # Update the origin for next time.
            self.last_x = e.x()
            self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.last_x = None
            self.last_y = None
            self.is_drawing = False
            #print(self.last_x, self.last_y, self.is_drawing)

    # def paintEvent(self, event):
    #     if self.lbl_canvas.pixmap() is not None:
    #         width = self.lbl_canvas.width()
    #         height = self.lbl_canvas.height()
    #         self.lbl_canvas.pixmap().scaled(width, height)
    #         #self.lbl_canvas.setPixmap(self.lbl_canvas.pixmap().scaled(width, height))
    #         #print("paint")

    def detect(self, image):
        if self.lbl_canvas.pixmap() is not None:
            if not self.is_detecting:
                self.is_detecting = True
                self.btn_detect.setText("Stop")

                self.last_state_image = QtGui.QPixmap(self.lbl_canvas.pixmap())

                self.switchDrawingMode(False)

                image = self.convertQImageToMat(self.lbl_canvas.pixmap())
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (7, 7), 0)
                thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 2)

                contours, hierarchy = cv2.findContours(thre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                offset = 10

                for i in contours:
                    # contours sẽ chỉ được tính nếu có kích thước lớn hơn 100 (nhằm loại bỏ các vật thể nhiễu)
                    if cv2.contourArea(i) < 100:
                        continue

                    # Hàm cv2.boundingRect() giúp tìm ra Bounding box hình chữ nhật đứng.
                    (x, y, w, h) = cv2.boundingRect(i)

                    # Vẽ hình chữ nhật bao quanh vật thể với bounding box vừa tìm được
                    cv2.rectangle(image, (x - offset, y - offset), (x + w + offset, y + h + offset), (0, 0, 255), 2)

                    # Lấy ra một ảnh chỉ chứa một vật thể dựa vào bounding box
                    # resize lại kích thước phù hợp với model để có thể dự đoán
                    roi = thre[y:y + h, x:x + w]
                    roi = np.pad(roi, (20, 20), 'constant', constant_values=(0, 0))
                    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
                    roi = cv2.dilate(roi, (3, 3))

                    # Hàm predict_classes trả về class có xác suất lớn nhất
                    #y_predict = self.model.predict_classes(roi.reshape(1, 28, 28, 1))
                    y_predict = np.argmax(self.model.predict(roi.reshape(1, 28, 28, 1)), axis=-1)

                    # Gắn chữ đã dự đoán được lên ảnh ban đầu
                    cv2.putText(image, str(chr(ord('A') + y_predict - 1)), (x, y - offset - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                1)

                # In ra ảnh đã được dự đoán tất cả các chữ viết
                #cv2.imshow('test',image)
                #cv2.waitKey()
                #cv2.destroyAllWindows()
                print(image.shape)
                self.showImage(self.lbl_canvas, image)
            else:
                self.is_detecting = False
                self.btn_detect.setText("Detect")
                self.switchDrawingMode(True)

                if self.last_state_image is not None:
                    self.lbl_canvas.setPixmap(self.last_state_image)
                else:
                    self.lbl_canvas.setPixmap(self.backup_image)

    def switchDrawingMode(self, switch: bool):
        self.btn_clear.setEnabled(switch)
        self.btn_open.setEnabled(switch)

    def changeBrushSize(self):
        self.pen_size = self.sbox_brush_size.value()

    def convertQImageToMat(self, pixmap = None):
        '''  Converts a QImage into an opencv MAT format  '''
        if pixmap is None:
            pixmap = self.image
        if pixmap is not None:
            if type(pixmap) is QtGui.QPixmap:
                new_qimage = pixmap.toImage().convertToFormat(QtGui.QImage.Format_RGBA8888)

            width = new_qimage.width()
            height = new_qimage.height()

            ptr = new_qimage.bits()
            ptr.setsize(new_qimage.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
            arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
            return arr

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tmp = Ui_MainWindow()
    app.exec_()
