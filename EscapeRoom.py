import sys
from PyQt6.QtWidgets import QApplication

from MainUI import MainUI
from StartupUI import StartupUI




if __name__ == '__main__': 
    app = QApplication(sys.argv)

    """
    myApp = StartupUI()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        myApp.destroy()
        print('Closing Window...')   
    """

    myApp = MainUI()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        myApp.destroy()
        print('Closing Window...')