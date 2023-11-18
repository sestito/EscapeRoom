import os
import sys
import time

from datetime import datetime, timedelta

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog, QWidget, QMainWindow, QButtonGroup, QMessageBox
from PyQt6.uic import loadUi

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget


def fix_time(disp_string: str):
    if len(disp_string) != 0:
        while disp_string[0] == '0' or disp_string[0] == ":":
            disp_string = disp_string[1:]
            if len(disp_string) == 0:
                break

    if disp_string == '':
        disp_string = '0'
    
    return disp_string

class MainUI(QMainWindow):
    ui_name: str = "MainUI.ui"
    video: str = "EscapeRoomIntro.mp4"
    debug = False
    fullscreen = True

    def __init__(self, data):
        self.data = data

        default_path = os.path.dirname(os.path.realpath(__file__))
        main_ui_file = os.path.join(default_path, self.ui_name)
        super().__init__()
        loadUi(main_ui_file, self)
        if self.fullscreen:
            self.showFullScreen()
        else:
            self.showMaximized()

        self.enable_code(False)
        self.codeStatus.setText("")
        self.confirmCode.setText("")
        

        self.media_player = QMediaPlayer()
        self.media_player.errorOccurred.connect(self._player_error)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        

        #self.video_widget = QVideoWidget()
       
        #self.media_player.play()

        #self.mainLayout.addWidget(self.video_widget)

        # Start Second
        start_time = data["TIMING"]["StartTime"]
        start_time = start_time.split(':')
        self.start_second = (int(start_time[0]) * 60 + int(start_time[1])) * 60


        #Timer Stuff
        # Second update timer
        self.preupdateTimer = QtCore.QTimer(self)
        self.preupdateTimer.setInterval(100)
        self.preupdateTimer.timeout.connect(self.PreTimerCallback)

        # Second update timer
        self.postupdateTimer = QtCore.QTimer(self)
        self.postupdateTimer.setInterval(100)
        self.postupdateTimer.timeout.connect(self.PostTimerCallback)

        

        # Oneshot timers
        self.textAppearTimer = QtCore.QTimer(self)
        self.textAppearTimer.setSingleShot(True)
        timeout = int(data["INTRO"]["TimeReappear"]) # Seconds
        timeout = timeout * 1000
        self.textAppearTimer.setInterval(timeout)
        self.textAppearTimer.timeout.connect(self.AppearIntroTimer)
        

        self.textStartTimer = QtCore.QTimer(self)
        self.textStartTimer.setSingleShot(True)
        timeout = int(data["INTRO"]["TimeAfterVideo"]) # Seconds
        timeout += int(data["INTRO"]["VideoLength"])
        timeout = timeout * 1000
        self.textStartTimer.setInterval(timeout)
        self.textStartTimer.timeout.connect(self.StartIntroTimer)

        self.startTTimer = QtCore.QTimer(self)
        self.startTTimer.setSingleShot(True)
        timeout = int(self.data["INTRO"]["TimeStartTimer"]) # Seconds
        timeout = timeout * 1000
        self.startTTimer.setInterval(timeout)
        self.startTTimer.timeout.connect(self.Start)


        timeout = int(data["INTRO"]["TimeAfterVideo"]) # Seconds
        timeout += int(data["INTRO"]["VideoLength"])
        timeout += int(data["INTRO"]["TimeStartTimer"])
        self.startTime = timeout


        self.confirmCode.clicked.connect(self.CheckCode)

        code_data = data["CODE"]
        self.code = code_data["Code"].upper()
        self.lockout_time = int(code_data["LockoutTime"])
        self.lockout_attempts = int(code_data["LockoutAttempts"])
        self.attempts = 0

        self.lockoutTimer = QtCore.QTimer(self)
        self.lockoutTimer.setSingleShot(True)
        timeout = int(code_data["LockoutTime"])
        timeout = timeout * 1000
        self.lockoutTimer.setInterval(timeout)
        self.lockoutTimer.timeout.connect(self.Unlock)


        self.statusResetTimer = QtCore.QTimer(self)
        self.statusResetTimer.setSingleShot(True)
        self.statusResetTimer.setInterval(5 * 1000)
        self.statusResetTimer.timeout.connect(self.SetDefaultStatus)

        
        self.SetTimerState()
        

        

    def SetTimerState(self):
        now = datetime.now()
        t = now.time()
        seconds = (t.hour * 60 + t.minute) * 60 + t.second
        if seconds < self.start_second:
            self.preupdateTimer.start()
        else:
            self.Start()

    def PostTimerCallback(self):
        now = datetime.now()
        t = now.time()
        seconds = (t.hour * 60 + t.minute) * 60 + t.second
        
        # After we start
        seconds_since_start = seconds - self.start_second
        seconds_left = int(self.data["TIMING"]["Duration"]) * 60 - seconds_since_start

        if seconds_left > 0:
            # We are in competition
            disp_string = str(timedelta(seconds = seconds_left))

        else:
            #ran out of time
            disp_string = 'Time up!'
            self.postupdateTimer.stop()
            self.End()
        
        if len(disp_string) != 0:
            while disp_string[0] == '0' or disp_string[0] == ":":
                disp_string = disp_string[1:]
                if len(disp_string) == 0:
                    break

        if disp_string == '':
            disp_string = '0'

        self.Clock.setText(disp_string)
    
    def PreTimerCallback(self):
        now = datetime.now()
        t = now.time()
        seconds = (t.hour * 60 + t.minute) * 60 + t.second
        


        if seconds < self.start_second:
            # Before we are supposed to start
            seconds_until_start = self.start_second - seconds
            #Make it start at the video time
            display_seconds = seconds_until_start
            display_seconds -= int(self.data["INTRO"]["VideoLength"])
            display_seconds -= int(self.data["INTRO"]["TimeAfterVideo"])
            display_seconds -= int(self.data["INTRO"]["TimeStartTimer"])
            disp_string = str(timedelta(seconds = display_seconds))

            # TODO: What do I do if I crash mid video?
            if seconds_until_start < self.startTime:
                self.StartSequence()
                return

        else:
            self.preupdateTimer.stop()
            self.Start()


        
        if len(disp_string) != 0:
            while disp_string[0] == '0' or disp_string[0] == ":":
                disp_string = disp_string[1:]
                if len(disp_string) == 0:
                    break

        if disp_string == '':
            disp_string = '0'

        self.Clock.setText(disp_string)



    def StartSequence(self):
        if self.debug: print('Initiate Start Sequence!')
        self.start_video(self.video)
        self.StopIntroTimer()
        self.textAppearTimer.start()
        self.textStartTimer.start()


    def StopIntroTimer(self):
        if self.debug: print('Stop Intro Timer')
        self.preupdateTimer.stop()
        self.Clock.setText("")

    def AppearIntroTimer(self):
        if self.debug: print('Appear Timer')
        time = int(self.data["TIMING"]["Duration"]) * 60
        disp_string = str(timedelta(seconds = time))
        disp_string = fix_time(disp_string)   
        self.Clock.setText(disp_string)

    def StartIntroTimer(self):
        if self.debug: print('Initiating Timer')
        # Play audio


        seconds_to_wait = int(self.data["INTRO"]["TimeStartTimer"])
        self.startTTimer.start()

    def Start(self):
        if self.debug: print('Starting Game')
        #unlock buttons
        self.enable_code()
        self.confirmCode.setText("Confirm Code")
        self.SetDefaultStatus()

        self.postupdateTimer.start()

    def End(self):
        # Lock code enter thing
        #self.lockoutTimer.stop()
        pass


    def CheckCode(self):
        self.update_status("Checking Code...")
        guess = self.codeEntry.text().upper()
        if guess == self.code:
            self.Win()
        else:
            self.attempts += 1
            # status wrong code
            self.WrongCodeStatus(guess)
            if self.attempts >= self.lockout_attempts:
                self.Lockout()
                self.attempts = 0

    def WrongCodeStatus(self, guess):
        self.update_status("Wrong Code!")

    def Lockout(self):
        self.statusResetTimer.stop()
        self.enable_code(False)
        self.update_status("Locked Out!")
        self.statusResetTimer.stop()
        self.lockoutTimer.start()

    def Unlock(self):
        self.enable_code(True)
        self.SetDefaultStatus()

    def Win(self):
        self.enable_code(False)
        self.postupdateTimer.stop()
        self.Clock.setText('You Win!')
        self.codeStatus.setText('You Win!')

    def SetDefaultStatus(self):
        self.codeStatus.setText("Awaiting Code...")

    def update_status(self, text):
        self.codeStatus.setText(text)
        self.statusResetTimer.stop()
        self.statusResetTimer.start()

    def enable_code(self, state = True):
        self.codeEntry.setEnabled(state)
        self.confirmCode.setEnabled(state)

    def start_video(self, video):
        default_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(default_path, video)

       
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self.media_player.setVideoOutput(self.video_player)
        self.media_player.play()
    
    #@Slot("QMediaPlayer::Error", str)
    def _player_error(self, error, error_string):
        print(error_string, file=sys.stderr)
        #self.show_status_message(error_string)