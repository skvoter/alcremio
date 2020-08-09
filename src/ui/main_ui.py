from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests
import qtawesome as qta
import ui.fonts_rc


def get_screen():
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    screenobj = QtWidgets.QApplication.desktop().screenGeometry(screen)
    return screenobj


class BackgroundArt(QtWidgets.QLabel):
    hover = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, *args, **kwargs)
        back = requests.get("https://i.scdn.co/image/ab67616d0000b273ab0b0448520d99ff0aa7b1eb").content
        backimage = QtGui.QImage.fromData(back)
        self.background = QtGui.QPixmap.fromImage(backimage)
        self.setPixmap(self.background.scaledToHeight(self.height()))
        self.setAlignment(QtCore.Qt.AlignCenter)


class Overlay(QtWidgets.QWidget):
    def __init__(self, parent):
        QtGui.QFontDatabase.addApplicationFont(":/fonts/Montserrat-Medium.ttf")
        QtWidgets.QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)
        self.controlWidgets = list()

    
    def hideOnMove(self):
        self.parent().animationHideOut.start()
    
    def showOnRelease(self):
        self.parent().animationShowOut.start()


class ControlWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.widget = qta.IconWidget()
        self.widget.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().addWidget(self.widget)
        self.widget.resize(39, 39)
        self.currentIconSize = QtCore.QSize(32,32)
        self.widget.setIconSize(self.iconsize)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(32, 32)
        if self.parent:
            self.parent().controlWidgets.append(self)
        self.animationZoomIn = QtCore.QPropertyAnimation(self, b"iconsize")
        self.animationZoomIn.setDuration(200)
        self.animationZoomIn.setStartValue(self.currentIconSize)
        self.animationZoomIn.setEndValue(QtCore.QSize(
            self.currentIconSize.width()*1.2,
            self.currentIconSize.height()*1.2
        ))
        self.animationZoomOut = QtCore.QPropertyAnimation(self, b"iconsize")
        self.animationZoomOut.setDuration(200)
        self.animationZoomOut.setStartValue(QtCore.QSize(
            self.currentIconSize.width()*1.2,
            self.currentIconSize.height()*1.2
        ))
        self.animationZoomOut.setEndValue(self.currentIconSize)
        

    def getIconSize(self):
        return self.currentIconSize
    
    def setIconSize(self, value):
        self.widget.setIconSize(value)
        self.widget.update()
        # self.currentIconSize = value
    
    iconsize = QtCore.pyqtProperty(QtCore.QSize, getIconSize, setIconSize)

    def enterEvent(self, event):
        self.animationZoomIn.start()
    
    def leaveEvent(self, event):
        self.animationZoomOut.start()
        


class CloseWidget(ControlWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.icon = qta.icon('fa5s.times')
        self.widget.setIcon(self.icon)

    def mousePressEvent(self, event):
        sys.exit(0)


class MoveWidget(ControlWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.icon = qta.icon('fa5s.expand')
        self.widget.setIcon(self.icon)

    def mousePressEvent(self, event):
        self.parent().hideOnMove()


    def mouseMoveEvent(self, event):
        center = self.frameGeometry().center()
        window = self.parent().parent()
        window.move(QtGui.QCursor().pos() - center)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.parent().showOnRelease()


class PlayPauseWidget(ControlWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.icon = qta.icon('fa5s.play')
        self.widget.setIcon(self.icon)

    def mousePressEvent(self, event):
        print('play')


class PrevWidget(ControlWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.icon = qta.icon('fa5s.step-backward')
        self.widget.setIcon(self.icon)

    def mousePressEvent(self, event):
        print('prev')


class NextWidget(ControlWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.icon = qta.icon('fa5s.step-forward')
        self.widget.setIcon(self.icon)

    def mousePressEvent(self, event):
        print('next')


class Ui_MainWindow(object):
    def setupLowLevel(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.backgroundArt = BackgroundArt(self.centralwidget)
        self.backgroundArt.setGeometry(QtCore.QRect(0, 0, self.initialSize.width(), self.initialSize.height()))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgroundArt.sizePolicy().hasHeightForWidth())
        self.backgroundArt.setSizePolicy(sizePolicy)
        self.backgroundArt.setText("")
        self.backgroundArt.setObjectName("backgroundArt")
        self.gridLayout.addWidget(self.backgroundArt, 0, 0, 0, 0)

    def setupOverlay(self):
        self.popup = Overlay(self)
        self.popup.setStyleSheet("* { color: black;} ")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.popup)
        self.gridLayout_2.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.setContentsMargins(20,20,20,20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.CloseButton = CloseWidget(self.popup)
        self.CloseButton.setObjectName("CloseButton")
        self.gridLayout_2.addWidget(
            self.CloseButton,
            0, 0, 1, 1,
            alignment=QtCore.Qt.AlignLeft
        )
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 3)
        self.MoveButton = MoveWidget(self.popup)
        self.MoveButton.setObjectName("MoveButton")
        self.gridLayout_2.addWidget(
            self.MoveButton,
            0, 4, 1, 1,
            alignment=QtCore.Qt.AlignRight
        )

        spacerItem3 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 1, 0, 1, 5)
    
        self.ArtistLabel = QtWidgets.QLabel(self.popup)
        self.ArtistLabel.setFont(QtGui.QFont("Montserrat", 24, QtGui.QFont.Bold))
        self.ArtistLabel.setObjectName("ArtistLabel")

        self.ArtistLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.ArtistLabel, 2, 0, 1, 5)

        
        self.SongLabel = QtWidgets.QLabel(self.popup)
        self.SongLabel.setFont(QtGui.QFont("Montserrat", 24, QtGui.QFont.Bold))

        self.SongLabel.setObjectName("SongLabel")
        self.SongLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.SongLabel.setText("hрусскийere is song title")
        self.ArtistLabel.setText("machine gun kelly")

        self.gridLayout_2.addWidget(self.SongLabel, 3, 0, 1, 5)
        self.prevButton = PrevWidget(self.popup)
        self.prevButton.setObjectName("prevButton")
        self.gridLayout_2.addWidget(
            self.prevButton,
            4, 0, 1, 2,
            alignment=QtCore.Qt.AlignRight    
        )
        self.playButton = PlayPauseWidget(self.popup)
        self.playButton.setObjectName("playButton")
        self.gridLayout_2.addWidget(
            self.playButton,
            4, 2, 1, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.nextButton = NextWidget(self.popup)
        self.nextButton.setObjectName("nextButton")
        self.gridLayout_2.addWidget(
            self.nextButton,
            4, 3, 1, 2,
            alignment=QtCore.Qt.AlignLeft
        )
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem6, 5, 1, 1, 1)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.screenSize = get_screen().size()
        height = int(self.screenSize.height()/3)
        self.initialSize = QtCore.QSize(height, height)
        MainWindow.resize(self.initialSize)
        MainWindow.setMinimumSize(QtCore.QSize(250, 250))
        MainWindow.setMaximumSize(QtCore.QSize(500,500))
        self.setupLowLevel(MainWindow)       
        self.setupOverlay()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("alcremio")