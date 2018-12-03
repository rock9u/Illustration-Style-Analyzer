import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap,QImage
import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ImageFilter import *
from PIL import Image
from PIL.ImageQt import ImageQt
# class MyMplCanvas(FigureCanvas):
#     """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         # We want the axes cleared every time plot() is called
#         self.axes.hold(False)

#         self.compute_initial_figure()

#         #
#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)

#         FigureCanvas.setSizePolicy(self,
#                                    QSizePolicy.Expanding,
#                                    QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)

#     def compute_initial_figure(self):
#         pass
# class MyStaticMplCanvas(MyMplCanvas):
#     """Simple canvas with a sine plot."""
#     def compute_initial_figure(self):
#         t = arange(0.0, 3.0, 0.01)
#         s = sin(2*pi*t)
#         self.axes.plot(plt_image)
#         # self.axes.plot(t, s)


# class MyDynamicMplCanvas(MyMplCanvas):
#     """A canvas that updates itself every second with a new plot."""
#     def __init__(self, *args, **kwargs):
#         MyMplCanvas.__init__(self, *args, **kwargs)
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(self.update_figure)
#         timer.start(1000)

#     def compute_initial_figure(self):
#         self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

#     def update_figure(self):
#         # Build a list of 4 random integers between 0 and 10 (both inclusive)
#         l = [random.randint(0, 10) for i in range(4)]

#         self.axes.plot([0, 1, 2, 3], l, 'r')
#         self.draw()

 
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
        self.input_confirm.clicked.connect(self.set_url)
        self.input_layout = QtWidgets.QHBoxLayout(self)
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_bar)
        self.input_layout.addWidget(self.input_confirm)

        content_layout.addLayout(self.input_layout)
        content_layout.addWidget(self.image_tab)

        self.setLayout(content_layout)

        self.show()

    def set_url(self):
        self.url = self.input_bar.text()
        # self.url = "https://wx2.sinaimg.cn/mw1024/bfee4305gy1ftsx96j7rrj22lk2ao4qq.jpg"
        self.img_filter = ImageFilter(self.url)
        self.computer_all_filters()

    def computer_all_filters(self):
        for mode in self.FILTERS_MODES:
            self.create_filter_tabs(mode)

        # Create widget
    def create_filter_tabs(self,mode):
        label = QLabel(self)
        saturation_filtered_img = self.img_filter.filter_hsv(mode)
        pixmap = QPixmap.fromImage(ImageQt(saturation_filtered_img.convert("RGBA")))
        label.setPixmap(pixmap)
        self.image_tab.addTab(label,mode)
        self.resize(pixmap.width(),pixmap.height())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())