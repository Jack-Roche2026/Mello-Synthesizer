from synthesizer import Synthesizer

class Explore():
    """_summary_ synthesizes sounds requested when in explore mode
    """
    def __init__(self, key, octave, waveform, level, duration):
        """_summary_ initializes attributes of sound as self variables, calls the note method to make the sound and play it

        Args:
            key (int): _description_ which key was pressed
            octave (int): _description_ which octave the keyboard was in when the key was pressed
            waveform (string): _description_ which waveform was selected when the key was pressed
            level (int): _description_ what level the keyboard was set to when the key was pressed
            duration (int): _description_ duration of the requested sound
        """
        self.key = key
        self.octave = octave
        self.waveform = waveform
        self.level = level
        self.duration = duration
        # calls the note method to play the requested sound
        self.note()

    def note(self):
        # creates a Synthesizer instance with the attributes of the requested sound
        note = Synthesizer(self.key, self.waveform, self.octave, self.level, self.duration)
        # synthesizes that instance
        Synthesizer.synthesize(note)
        # plays that instance
        Synthesizer.playthis(note)
