from pydub import AudioSegment
from pydub.playback import play
import os

class RealTime():
    """_summary_ gets information about sound, then finds the premade file of that sound and plays it
    """
    def __init__(self, key, octave):
        """_summary_ initializes variables and calls the note method to play sound

        Args:
            key (int): _description_ which note in the octave we played
            octave (int): _description_ which octave on the keyboard
        """
        # initializes variables
        self.key = key
        self.octave = octave
        # calls method to find and play sound
        self.note()

    def note(self):
        """_summary_ finds premade wav file with sound attributes and plays it
        """
        # finds what the file name of a sound with these attributes would be
        self.filename = os.path.abspath(f'Mello Synth/Premade Files/o{self.octave}k{self.key}.wav')
        # reads the file
        self.sound = AudioSegment.from_wav(self.filename)
        # plays the files
        play(self.sound)