from synthesizer import Synthesizer

class Keyboard():
    """_summary_ parent to octave and grandparent to key, used to change variables when buttons are pressed
    """
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#']
    octaves = [1,2,3,4,5,6,7]

    def __init__(self, mode, waveform, level):
        """_summary_ initializes variables depending on what mode the keyboard is in

        Args:
            mode (string): _description_ controls how the sound is played
            waveform (string): _description_ controls the "sound" of the sound
            level (int): _description_ controls the volume of the sound
        """

        # switching between modes of the keyboard
        self.mode = mode
        if self.mode == 'Explore Mode':
            self.waveform = waveform
            self.level = level
            return
        if self.mode == 'Real Time Mode':
            self.level = -5
            self.waveform = 'Sine'
            return

class Octave(Keyboard):
    """_summary_ used primarily for organization

    Args:
        Keyboard (class): _description_ encompasses all octaves on the keyboard
    """
    def __init__(self, mode, waveform, level, octave):
        """_summary_ initializes the variables, brings the variables down from the keyboard class

        Args:
            mode (string): _description_ controls how the sound is played
            waveform (string): _description_ controls the "sound" of the sound
            level (int): _description_ controls the volume of the sound
            octave (int): _description_ controls what window we are in on the grand piano
        """
        super().__init__(mode, waveform, level)

        # gets the octave number
        self.octave = octave

    def octave_up(self):
        """_summary_ increases octave by 1
        """
        # increases octave if within range of 1-7
        if self.octave < 7:
            self.octave += 1

    def octave_down(self):
        """_summary_ decreases octave by 1
        """
        # decreases octave if within range of 1-7
        if self.octave > 1:
            self.octave -= 1

class Key(Octave):
    """_summary_ child of octave, grandchild of keyboard

    Args:
        Octave (class): _description_ gets the octave number, and all other variables from keyboard function
    """
    def __init__(self, mode, waveform, level, octave, key, duration):
        """_summary_

        Args:
            mode (string): _description_ controls how the sound is played
            waveform (string): _description_ controls the "sound" of the sound
            level (int): _description_ controls the volume of the sound
            octave (int): _description_ controls what window we are in on the grand piano
            key (int): _description_ which note in the octave we play
            duration (int): _description_ amount of time the sound will play for
        """
        super().__init__(mode, waveform, level, octave)

        # gets duration from key time
        self.duration = duration

        # gets the note name from the key number
        if key == 1:
            self.key = 'C'
            return
        elif key == 2:
            self.key = 'C#'
            return
        elif key == 3:
            self.key = 'D'
            return
        elif key == 4:
            self.key = 'D#'
            return
        elif key == 5:
            self.key = 'E'
            return
        elif key == 6:
            self.key = 'F'
            return
        elif key == 7:
            self.key = 'F#'
            return
        elif key == 8:
            self.key = 'G'
            return
        elif key == 9:
            self.key = 'G#'
            return
        elif key == 10:
            self.key = 'A'
            return
        elif key == 11:
            self.key = 'A#'
            return
        elif key == 12:
            self.key = 'B'
            return

    def __str__(self):
        """_summary_ returns a string describing the note

        Returns:
            string: _description_ musical representation of what key you pressed
        """
        # gets the string name of the note
        return f'{self.key}{self.octave}'

    def make(self):
        """_summary_ generates and plays a sound with the given attributes
        """
        # creates instance of synthesizer with given attributes
        note = Synthesizer(self.key, self.waveform, self.octave, self.level, self.duration)
        # generates sound, plays sound of instance
        Synthesizer.synthesize(note)
        Synthesizer.playthis(note)