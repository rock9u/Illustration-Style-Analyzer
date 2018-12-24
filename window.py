import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QScrollArea, QLabel
from PyQt5.QtGui import QIcon, QPixmap,QImage, QPalette
import sys
import random
from PyQt5 import QtCore, QtWidgets,QtGui
from numpy import arange, sin, pi
from ImageFilter import *
from PIL import Image, ImageGrab
from PIL.ImageQt import ImageQt
 
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Illustration Style Analyzer'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.FILTERS_MODES = [
            'original',
            'saturation',
            'greyscale' ,
            'value' ,
            'polarize'  ,
        ]
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.image_tab = QtWidgets.QTabWidget(self)
        content_layout = QtWidgets.QVBoxLayout(self)
        self.sidebar_layout = QtWidgets.QHBoxLayout(self)

        self.input_label = QtWidgets.QLabel(self)
        self.input_label.setText("URL:")
        self.input_bar = QtWidgets.QLineEdit(self)
        self.input_confirm = QtWidgets.QPushButton(self)
        self.input_confirm.setText("OK")
        self.input_confirm.clicked.connect(self.analyze_from_url)

        self.clipboard_confirm = QtWidgets.QPushButton(self)
        self.clipboard_confirm.setText("From Clipboard")
        self.clipboard_confirm.clicked.connect(self.analyze_from_clipboard)

        self.input_layout = QtWidgets.QHBoxLayout(self)
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_bar)
        self.input_layout.addWidget(self.input_confirm)
        self.input_layout.addWidget(self.clipboard_confirm)

        content_layout.addLayout(self.input_layout)
        content_layout.addWidget(self.image_tab)

        self.setLayout(content_layout)

        self.show()

    def analyze_from_url(self):
        self.url = self.input_bar.text()
        if self.url == '':
            self.url = "https://wx2.sinaimg.cn/mw1024/bfee4305gy1ftsx96j7rrj22lk2ao4qq.jpg"
        try:
            self.img_filter = ImageFilter(url=self.url)
        except Exception as e:
            self.show_warning(str(e))
            return
        self.computer_all_filters()

    def analyze_from_clipboard(self):
        try:
            img = ImageGrab.grabclipboard()
            self.img_filter = ImageFilter(image=img)
        except Exception as e:
            self.show_warning(str(e))
            return
        self.computer_all_filters()

    def computer_all_filters(self):
        self.image_tab.clear()
        for mode in self.FILTERS_MODES:
            self.create_filter_tabs(mode)

        # Create widget
    def create_filter_tabs(self,mode):
        label = QLabel(self)
        saturation_filtered_img = self.img_filter.filter_hsv(mode)
        pixmap = QPixmap.fromImage(ImageQt(saturation_filtered_img.convert("RGBA")))
        label.setPixmap(pixmap)
        label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(label)
        scrollArea.widgetResizable=True

        self.image_tab.addTab(scrollArea,mode)
        self.resize(pixmap.width(),pixmap.height())
 
    def show_warning(self,text):
        warning = QtWidgets.QMessageBox()
        warning.setText(text)
        warning.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())