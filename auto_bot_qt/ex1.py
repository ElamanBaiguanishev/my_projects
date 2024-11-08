from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("MCVE")

        """Window Background"""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkYellow)
        self.setPalette(p)

        """Core Layouts"""
        self.mainLayout = QGridLayout()
        self.picLayout = QHBoxLayout()
        self.redditSubs = QVBoxLayout()
        self.downloadBar = QHBoxLayout()
        self.profileInfo = QGridLayout()

        """Nested Layout"""
        self.mainLayout.addLayout(self.profileInfo, 0, 0)
        self.mainLayout.addLayout(self.picLayout, 0, 1)
        self.mainLayout.addLayout(self.redditSubs, 1, 0)
        self.mainLayout.addLayout(self.downloadBar, 1, 1)

        """Widgets"""
        self.display = QLabel("QHBoxLayout()")
        self.download = QLabel("QHBoxLayout()")
        self.subs = QLabel("QVBoxLayout()")

        self.fileInfo = QLabel("QGridLayout()")

        self.panel = QWidget()

        """AddWidgets"""
        self.picLayout.addWidget(self.display)
        self.downloadBar.addWidget(self.download)
        self.redditSubs.addWidget(self.subs)
        self.profileInfo.addWidget(self.panel, 0, 0)

        lay = QVBoxLayout(self.panel)
        lay.addWidget(self.fileInfo)

        """Stylesheet"""
        self.panel.setStyleSheet("background-color: red;")

        """Initiating  mainLayout """
        self.window = QWidget()
        self.window.setLayout(self.mainLayout)
        self.setCentralWidget(self.window)


if __name__ == "__main__":
    app = QApplication([])
    w = Window()
    w.showNormal()
    app.exec_()