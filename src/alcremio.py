import sys
from PyQt5 import QtWidgets, QtCore, QtGui


import ui.main

class Alcremio(QtWidgets.QMainWindow, ui.main.Ui_MainWindow):
    def __init__(self, parent=None, flags=QtCore.Qt.WindowFlags()):
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        super().__init__(parent=parent, flags=flags)
        self.setupUi(self)
        self.popup.hide()
        # self.label.hover.connect(self.displayOverlay)
        self.effect = QtWidgets.QGraphicsBlurEffect()
        self.effect.setBlurRadius(0)
        self.animationBlurIn = QtCore.QPropertyAnimation(self.effect, b"blurRadius")
        self.animationBlurOut = QtCore.QPropertyAnimation(self.effect, b"blurRadius")
        self.label.setGraphicsEffect(self.effect)
        self.animationBlurIn.setDuration(500)
        self.animationBlurIn.setStartValue(0)
        self.animationBlurIn.setEndValue(15)
        self.animationBlurOut.setDuration(500)
        self.animationBlurOut.setStartValue(15)
        self.animationBlurOut.setEndValue(0)

    def enterEvent(self, event):
        if not self.animationBlurOut.Stopped:
            val = self.animationBlurOut.currentValue()
            self.animationBlurOut.stop()
            self.animationBlurIn.setStartValue(val)
        self.animationBlurIn.start()
        self.displayOverlay()

    def leaveEvent(self, event):
        if not self.animationBlurIn.Stopped:
            val = self.animationBlurIn.currentValue()
            self.animationBlurIn.stop()
            self.animationBlurOut.setStartValue(val)
        self.animationBlurOut.start()

    def resizeEvent(self, event):
        print(event.size())
        print("GRID ", self.gridLayout.sizeHint())
        super().resizeEvent(event)
        self.label.setPixmap(self.background.scaledToHeight(self.label.height()))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.popup.resize(event.size())
        event.accept()
    
    def displayOverlay(self):
        self.popup.show()
        print("clicked")


    
    # def mousePressEvent(self, event):
    #     self.mpos = event.pos()
    #     return super().mousePressEvent(event)
    
    # def mouseMoveEvent(self, event):
    #     if event.buttons() and QtCore.Qt.LeftButton:
    #         diff = event.pos() - self.pos()
    #         newpos = self.pos() + diff
    #         self.move(newpos)
    #     return super().mouseMoveEvent(event)

def main():
    print("started")
    app = QtWidgets.QApplication([])
    window = Alcremio()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()