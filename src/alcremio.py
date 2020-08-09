import sys
from PyQt5 import QtWidgets, QtCore, QtGui


import ui.main_ui
import warnings

from gi.repository import Playerctl, GLib


class PlayerThread(QtCore.QThread):

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window
    
    def run(self):

        self.player = Playerctl.Player()
        self.player.connect('metadata', self.on_metadata)


    def on_metadata(self, player, metadata):
        if 'xesam:artist' in metadata.keys() and 'xesam:title' in metadata.keys():
            print('Now playing:')
            print('{artist} - {title}'.format(artist=metadata['xesam:artist'][0],
                                            title=metadata['xesam:title']))


class Alcremio(QtWidgets.QMainWindow, ui.main_ui.Ui_MainWindow):
    def __init__(self, parent=None, flags=QtCore.Qt.WindowFlags()):
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        super().__init__(parent=parent, flags=flags)
        self.setupUi(self)
        self.setupAnimaions()
        self.playerThread = PlayerThread(self)
        self.center()
        self.playerThread.run()


    def setupAnimaions(self):
        self.effect = QtWidgets.QGraphicsBlurEffect()
        self.effect.setBlurRadius(0)
        self.animationBlurIn = QtCore.QPropertyAnimation(self.effect, b"blurRadius")
        self.animationBlurOut = QtCore.QPropertyAnimation(self.effect, b"blurRadius")
        self.backgroundArt.setGraphicsEffect(self.effect)
        self.animationBlurIn.setDuration(500)
        self.animationBlurIn.setStartValue(0)
        self.animationBlurIn.setEndValue(15)
        self.animationBlurOut.setDuration(500)
        self.animationBlurOut.setStartValue(15)
        self.animationBlurOut.setEndValue(0)
        self.overlayeffect = QtWidgets.QGraphicsOpacityEffect()
        self.overlayeffect.setOpacity(0.0)
        self.animationShowOut = QtCore.QPropertyAnimation(self.overlayeffect, b"opacity")
        self.animationHideOut = QtCore.QPropertyAnimation(self.overlayeffect, b"opacity")
        self.popup.setGraphicsEffect(self.overlayeffect)
        self.animationShowOut.setDuration(500)
        self.animationShowOut.setStartValue(0.0)
        self.animationShowOut.setEndValue(1.0)
        self.animationHideOut.setDuration(500)
        self.animationHideOut.setStartValue(1.0)
        self.animationHideOut.setEndValue(0.0)
        print(self.popup.controlWidgets)

    def center(self):
        frameGm = self.frameGeometry()
        screenobj = ui.main_ui.get_screen()
        centerPoint = screenobj.center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def enterEvent(self, event):
        if not self.animationBlurOut.Stopped:
            val = self.animationBlurOut.currentValue()
            self.animationBlurOut.stop()
            self.animationBlurIn.setStartValue(val)
        self.animationBlurIn.start()
        if not self.animationHideOut.Stopped:
            val = self.animationHideOut.currentValue()
            self.animationHideOut.stop()
            self.animationShowOut.setStartValue(val)
        self.animationShowOut.start()


    def leaveEvent(self, event):
        if not self.animationBlurIn.Stopped:
            val = self.animationBlurIn.currentValue()
            self.animationBlurIn.stop()
            self.animationBlurOut.setStartValue(val)
        self.animationBlurOut.start()
        if not self.animationShowOut.Stopped:
            val = self.animationShowOut.currentValue()
            self.animationShowOut.stop()
            self.animationHideOut.setStartValue(val)
        self.animationHideOut.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.backgroundArt.setPixmap(self.backgroundArt.background.scaledToHeight(self.backgroundArt.height()))
        self.backgroundArt.setAlignment(QtCore.Qt.AlignCenter)
        self.popup.resize(event.size())
        event.accept()


def main():
    print("started")
    app = QtWidgets.QApplication([])
    window = Alcremio()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()