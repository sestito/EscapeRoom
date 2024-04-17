import sys
import os
from PyQt6.QtWidgets import QApplication

from MainUI import MainUI

import configparser


if __name__ == '__main__': 
    config = configparser.ConfigParser()
    default_path = os.path.dirname(os.path.realpath(__file__))
    config.read(os.path.join(default_path,'config.ini'))

    app = QApplication(sys.argv)

    myApp = MainUI(config)
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        myApp.destroy()
        print('Closing Window...')