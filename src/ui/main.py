# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import resources_rc
import requests

class BackgroundArt(QtWidgets.QLabel):
    hover = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, *args, **kwargs)
    #     self.effect = QtWidgets.QGraphicsBlurEffect()
    #     self.effect.setBlurRadius(0)
    #     self.animationBlurIn = QtCore.QPropertyAnimation(self.effect, b"blurRadius")
    #     self.animationBlurOut = QtCore.QPropertyAnimation(self.effect, b"blurRadius")
    #     self.setGraphicsEffect(self.effect)
    #     self.animationBlurIn.setDuration(500)
    #     self.animationBlurIn.setStartValue(0)
    #     self.animationBlurIn.setEndValue(15)
    #     self.animationBlurOut.setDuration(500)
    #     self.animationBlurOut.setStartValue(15)
    #     self.animationBlurOut.setEndValue(0)

    # def enterEvent(self, event):
    #     if not self.animationBlurOut.Stopped:
    #         val = self.animationBlurOut.currentValue()
    #         self.animationBlurOut.stop()
    #         self.animationBlurIn.setStartValue(val)
    #     self.animationBlurIn.start()
    #     self.hover.emit(1)

    # def leaveEvent(self, event):
    #     if not self.animationBlurIn.Stopped:
    #         val = self.animationBlurIn.currentValue()
    #         self.animationBlurIn.stop()
    #         self.animationBlurOut.setStartValue(val)
    #     self.animationBlurOut.start()

class CtmWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)

        self.button = QtWidgets.QPushButton("X")
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.button)

        self.button.clicked.connect(self.hideOverlay)

    # def paintEvent(self, event):

    #     painter = QtGui.QPainter()
    #     painter.begin(self)
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing)
    #     path = QtGui.QPainterPath()
    #     path.addRoundedRect(QtCore.QRectF(self.rect()), 10, 10)
    #     mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
    #     pen = QtGui.QPen(QtCore.Qt.white, 1)
    #     painter.setPen(pen)
    #     painter.fillPath(path, QtCore.Qt.white)
    #     painter.drawPath(path)
    #     painter.end()

    def hideOverlay(self):
        self.parent().hide()
        sys.exit(0)


class Overlay(QtWidgets.QWidget):
    def __init__(self, parent, widget):
        QtWidgets.QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)

        self.widget = widget
        self.widget.setParent(self)


    # def paintEvent(self, event):
    #     painter = QtGui.QPainter()
    #     painter.begin(self)
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing)
    #     painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(0, 0, 0, 127)))
    #     painter.end()

    # def resizeEvent(self, event):
    #     position_x = (self.frameGeometry().width()-self.widget.frameGeometry().width())/2
    #     position_y = (self.frameGeometry().height()-self.widget.frameGeometry().height())/2

    #     self.widget.move(position_x, position_y)
    #     event.accept()
def get_screen_size():
    sizeObject = QtWidgets.QDesktopWidget().screenGeometry(0)
    return sizeObject.size()
    

class Ui_MainWindow(object):
    def setupLowLevel(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = BackgroundArt(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, self.initialSize.width(), self.initialSize.height()))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        back = requests.get("https://i.stack.imgur.com/jpu4S.png").content
        backimage = QtGui.QImage.fromData(back)
        self.background = QtGui.QPixmap.fromImage(backimage)
        self.label.setPixmap(self.background.scaledToHeight(self.label.height()))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 0, 0)

    def setupOverlay(self):
        self.popup = Overlay(self, CtmWidget())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.screenSize = get_screen_size()
        # min size: 200x200m ideal 500x500 on 2k screen
        height = int(self.screenSize.height()/3)
        self.initialSize = QtCore.QSize(height, height)
        MainWindow.move(1, 1)
        MainWindow.resize(self.initialSize)
        MainWindow.setMinimumSize(QtCore.QSize(200, 200))
        self.setupLowLevel(MainWindow)       
        self.setupOverlay()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
