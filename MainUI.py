import os
import sys

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog, QWidget, QMainWindow, QButtonGroup, QMessageBox
from PyQt6.uic import loadUi

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

class MainUI(QMainWindow):
    ui_name = "MainUI.ui"

    def __init__(self, data):
        self.data = data

        default_path = os.path.dirname(os.path.realpath(__file__))
        main_ui_file = os.path.join(default_path, self.ui_name)
        super().__init__()
        loadUi(main_ui_file, self)



        self.media_player = QMediaPlayer()
        self.media_player.errorOccurred.connect(self._player_error)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        

        #self.video_widget = QVideoWidget()
       
        #self.media_player.play()

        #self.mainLayout.addWidget(self.video_widget)


        self.pushButton.clicked.connect(self.start_video)
        


    def start_video(self):
        default_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(default_path, "Countdown.mp4")

       
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self.media_player.setVideoOutput(self.video_player)
        self.media_player.play()
    
    #@Slot("QMediaPlayer::Error", str)
    def _player_error(self, error, error_string):
        print(error_string, file=sys.stderr)
        #self.show_status_message(error_string)