import os

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog, QWidget, QMainWindow, QButtonGroup, QMessageBox
from PyQt6.uic import loadUi

class StartupUI(QMainWindow):
    ui_name = "MainUI.ui"

    def __init__(self):
        default_path = os.path.dirname(os.path.realpath(__file__))
        main_ui_file = os.path.join(default_path, self.ui_name)
        super().__init__()
        loadUi(main_ui_file, self)