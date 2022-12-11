from ui import MelloSynth
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import os

class BootUp():
    """_summary_ starts the program, to run the application you need to run this file
    """
    def __init__(self):
        # initiates the app
        app = QApplication(sys.argv)
        # tells the app what icon to use
        app.setWindowIcon(QIcon(os.path.abspath(f'MellowSynth.ico')))
        # tells the app what to use as the window
        window = MelloSynth()
        window.show()
        # provides an exit option
        app.exec()