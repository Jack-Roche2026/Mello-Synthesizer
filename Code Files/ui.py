import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QRadioButton, QSlider, QLabel
from PyQt6.QtGui import QIcon
import os
from PyQt6.QtCore import Qt
from organizer import Keyboard, Key
from realtimemode import RealTime
from exploremode import Explore
from PyQt6.QtWidgets import QApplication

class MelloSynth(QWidget):
    """_summary_ the ui of the application

    Args:
        QWidget (class): _description_ the software that makes this ui possible
    """
    def __init__(self):
        """_summary_ sets the default variables, sets the icon, creates an instance of keyboard to store the attributes at any point, calls the rest of the ui setup
        """
        super().__init__()
        # sets icon
        app.setWindowIcon(QIcon(os.path.expanduser(f'~/Desktop/EECE 2140/Mello Synth/Premade Files/MellowSynth.ico')))
        # app.setWindowIcon(QIcon(os.path.abspath(f'/Premade Files/MellowSynth.ico')))
        # sets default attributes
        self.mode = 'PLEASE SELECT MODE'
        self.waveform = 'Sine'
        self.level = -20
        self.octave = 4
        self.duration = 1
        self.keyboard = Keyboard(self.mode, self.waveform, self.level)
        # calls the rest of the ui setup
        self.initUI()

    def initUI(self):
        """_summary_ takes care of the overarching basic setup
        """
        # sets window title and icon, sets size
        self.setWindowTitle('Mello Synthesizer')
        self.setWindowIcon(QIcon(os.path.expanduser(f'~/Desktop/EECE 2140/Mello Synth/Premade Files/MellowSynth.ico')))
        # self.setWindowIcon(QIcon(os.path.abspath(f'/Premade Files/MellowSynth.ico')))
        self.resize(50, 50) # width, height (just to make it as compact as possible, not actual size)


        # sets orientation of overall layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # calls the rest of the ui setup
        self.init_labels()
        self.init_settings()
        self.init_keys()

    def init_labels(self):
        """_summary_ generates the labels at the top of the ui
        """
        # creates labels layout and adds it to overall layout
        labels = QHBoxLayout()
        self.layout.addLayout(labels)

        # creates individual labels and adds them to the labels layout
        self.waveform_label = QLabel('Waveform')
        labels.addWidget(self.waveform_label)

        self.octave_label = QLabel(f'                                                                         Octave {self.octave}')
        labels.addWidget(self.octave_label)

        self.mode_label = QLabel(f'                                                   {self.mode}')
        labels.addWidget(self.mode_label)

        self.level_label = QLabel('                                          Volume Level Slider')
        labels.addWidget(self.level_label)

    def init_keys(self):
        """_summary_ makes all the key buttons
        """
        # creates key layout and adds it to overall layout
        keys = QHBoxLayout()
        self.layout.addLayout(keys)

        # keys
        w1 = QPushButton('C', clicked = self.send_to_mode)
        b2 = QPushButton('C#', clicked = self.send_to_mode)
        w3 = QPushButton('D', clicked = self.send_to_mode)
        b4 = QPushButton('D#', clicked = self.send_to_mode)
        w5 = QPushButton('E', clicked = self.send_to_mode)
        w6 = QPushButton('F', clicked = self.send_to_mode)
        b7 = QPushButton('F#', clicked = self.send_to_mode)
        w8 = QPushButton('G', clicked = self.send_to_mode)
        b9 = QPushButton('G#', clicked = self.send_to_mode)
        w10 = QPushButton('A', clicked = self.send_to_mode)
        b11 = QPushButton('A#', clicked = self.send_to_mode)
        w12 = QPushButton('B', clicked = self.send_to_mode)

        # adding each key as widget
        keys.addWidget(w1)
        keys.addWidget(b2)
        keys.addWidget(w3)
        keys.addWidget(b4)
        keys.addWidget(w5)
        keys.addWidget(w6)
        keys.addWidget(b7)
        keys.addWidget(w8)
        keys.addWidget(b9)
        keys.addWidget(w10)
        keys.addWidget(b11)
        keys.addWidget(w12)

    def init_settings(self):
        """_summary_ creates the layout for all settings that user can change
        """
        # creates settings layout and adds it to overall layout
        settings = QHBoxLayout()
        self.layout.addLayout(settings)

        # Waveform button(s)
        waveform = QVBoxLayout()
        settings.addLayout(waveform)

        self.sine = QRadioButton('Sine', self)
        self.sine.setChecked(True)
        self.sine.toggled.connect(self.change_waveform)
        waveform.addWidget(self.sine)
 
        self.square = QRadioButton('Square', self)
        self.square.toggled.connect(self.change_waveform)
        waveform.addWidget(self.square)

        self.triangle = QRadioButton('Triangle', self)
        self.triangle.toggled.connect(self.change_waveform)
        waveform.addWidget(self.triangle)

        self.sawtooth = QRadioButton('Sawtooth', self)
        self.sawtooth.toggled.connect(self.change_waveform)
        waveform.addWidget(self.sawtooth)

        # Change octaves
        octave = QVBoxLayout()
        settings.addLayout(octave)

        self.octave_up = QPushButton('Octave Up', clicked = self.change_octave)
        octave.addWidget(self.octave_up)

        self.octave_down = QPushButton('Octave Down', clicked = self.change_octave)
        octave.addWidget(self.octave_down)

        # Mode
        mode = QVBoxLayout()
        settings.addLayout(mode)

        self.mode = QPushButton('Switch to Real Time Mode', clicked = self.change_mode)
        mode.addWidget(self.mode)

        self.mode = QPushButton('Switch to Explore Mode', clicked = self.change_mode)
        mode.addWidget(self.mode)

        # level (loudness)
        levels = QVBoxLayout()
        settings.addLayout(levels)

        self.levellabel = QLabel('-20dB', self)
        levels.addWidget(self.levellabel)

        self.level_widget = QSlider(Qt.Orientation.Vertical, self)
        self.level_widget.setMaximum(0)
        self.level_widget.setMinimum(-50)
        self.level_widget.setValue(-20)
        self.level_widget.setTickInterval(2)
        self.level_widget.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.level_widget.valueChanged.connect(self.level_change)

        levels.addWidget(self.level_widget)

    def change_waveform(self):
        """_summary_ takes input from the waveform buttons and uses it to actually change the waveform
        """
        # each block checks which button was pressed, then changes the waveform to that button
        if self.sender().text() == 'Sine':
            self.waveform = self.sender().text()
            self.keyboard = Keyboard(self.mode, 'Sine', self.level)
            return
        elif self.sender().text() == 'Square':
            self.waveform = self.sender().text()
            self.keyboard = Keyboard(self.mode, 'Square', self.level)
            return
        elif self.sender().text() == 'Triangle':
            self.waveform = self.sender().text()
            self.keyboard = Keyboard(self.mode, 'Triangle', self.level)
            return
        else:
            self.waveform = self.sender().text()
            self.keyboard = Keyboard(self.mode, 'Sawtooth', self.level)
            return

    def change_octave(self):
        """_summary_ takes input from user to change the octave
        """
        # checks which button was pressed, then either increases or decreases the octave by 1
        if self.sender().text() == 'Octave Up' and self.octave < 7:
            self.octave += 1
            self.octave_label.setText((f'                                                                                                      Octave {self.octave}'))
            return
        elif self.sender().text() == 'Octave Down' and self.octave > 1:
            self.octave -= 1
            self.octave_label.setText((f'                                                                                                      Octave {self.octave}'))
            return

    def change_mode(self):
        """_summary_ changes the mode of the app
        """
        # if we switch to explore mode, the user needs all the settings at their disposal, so we show them all
        if self.sender().text() == 'Switch to Explore Mode':
            self.mode = 'Explore Mode'
            self.keyboard = Keyboard('Explore Mode', self.waveform, self.level)
            self.mode_label.setText((f'                                 {self.mode}'))
            self.waveform_label.show()
            self.levellabel.show()
            self.level_widget.show()
            self.level_label.show()
            self.sine.show()
            self.square.show()
            self.triangle.show()
            self.sawtooth.show()
            return
        # if we switch to real time mode, the user doesn't need the level or waveform settings anymore so we hide them
        else:
            self.mode = 'Real Time Mode'
            self.keyboard = Keyboard('Real Time Mode', self.waveform, self.level)
            self.mode_label.setText((f'                                 {self.mode}'))
            self.waveform_label.hide()
            self.levellabel.hide()
            self.level_widget.hide()
            self.level_label.hide()
            self.sine.hide()
            self.square.hide()
            self.triangle.hide()
            self.sawtooth.hide()
            return

    def level_change(self):
        """_summary_ changes the level based on the input of the slider
        """
        # changes the text of the label to show the user what the value of the slider is
        self.levellabel.setText(str(self.sender().value()) + 'dB')
        # changes the level to the new level value
        self.level = self.sender().value()
        self.keyboard = Keyboard(self.mode, self.waveform, self.level)

    def send_to_mode(self):
        """_summary_ takes key input and tells the proper mode to play a sound with the current attributes
        """
        # checks the key name, sets the key value to be the correct number for that key
        if self.sender().text() == 'C':
            self.key = 1
        if self.sender().text() == 'C#':
            self.key = 2
        if self.sender().text() == 'D':
            self.key = 3
        if self.sender().text() == 'D#':
            self.key = 4
        if self.sender().text() == 'E':
            self.key = 5
        if self.sender().text() == 'F':
            self.key = 6
        if self.sender().text() == 'F#':
            self.key = 7
        if self.sender().text() == 'G':
            self.key = 8
        if self.sender().text() == 'G#':
            self.key = 9
        if self.sender().text() == 'A':
            self.key = 10
        if self.sender().text() == 'A#':
            self.key = 11
        if self.sender().text() == 'B':
            self.key = 12

        # creates key instance to display the note we played in string form
        name = Key(self.mode, self.waveform, self.level, self.octave, self.key, self.duration)
        print(str(name))

        # sends information to the correct mode class which then makes sound
        if self.mode == 'Real Time Mode':
            RealTime(self.key, self.octave)
        if self.mode == 'Explore Mode':
            print(self.key, self.octave, self.waveform, self.level, self.duration)
            Explore(self.key, self.octave, self.waveform, self.level, self.duration)

# code to start the application
app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.abspath(f'MellowSynth.ico')))
window = MelloSynth()
window.show()
app.exec()