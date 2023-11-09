import os

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog, QWidget, QMainWindow, QButtonGroup, QMessageBox
from PyQt6.uic import loadUi

from PyQt6.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt6.QtMultimediaWidgets import QVideoWidget

class MainUI(QMainWindow):
    ui_name = "MainUI.ui"

    def __init__(self):
        default_path = os.path.dirname(os.path.realpath(__file__))
        main_ui_file = os.path.join(default_path, self.ui_name)
        super().__init__()
        loadUi(main_ui_file, self)

        self.media_player = QMediaPlayer()
        self.media_player.setSource("video.mp4")
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)