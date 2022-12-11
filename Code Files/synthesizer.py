import numpy as np
import scipy.io.wavfile as wav
import os
from pydub import AudioSegment
from pydub.playback import play
import math

class Synthesizer():
    """_summary_ generates sound, plays sound
    """
    def __init__(self, key, waveform, octave, level, duration):
        """_summary_ initializes all attributes as variables in the class

        Args:
            key (int): _description_ which note was played in the octave
            waveform (string): _description_ what type of sound we synthesize
            octave (int): _description_ which octave we play in the keyboard
            level (int): _description_ loudness of the sound
            duration (int): _description_ length of the sound in time
        """
        # initializing variables
        self.key = key
        self.waveform = waveform
        self.octave = octave
        self.level = level
        self.duration = duration
        # to get the frequency and file name from input variables
        self.get_frequency()
        self.__str__()
        return

    def __str__(self):
        """_summary_ returns a string with the filename of the sound

        Returns:
            string: _description_ file name of the sound
        """
        # finds filename to use as name of sound
        self.filename = os.path.abspath(f'{self.waveform}{self.frequency}Hz{self.duration}s{self.level}.wav')
        # self.filename = os.path.expanduser(f'~/Desktop/EECE 2140/Mello Synth/User Files/{self.waveform}{self.frequency}Hz{self.duration}s{self.level}.wav')
        # self.filename = os.path.expanduser(f'~/Desktop/EECE 2140/Mello Synth/Premade Files/o{self.octave}k{self.key}.wav')
        return self.filename

    def get_frequency(self):
        """_summary_ calculates the frequency we need to synthesize based on the octave and the key

        Returns:
            float: _description_ frequency of the desired note
        """
        # converts from key number of my keyboard to the key number of a grand piano
        total_key = (self.octave * 12) + self.key
        # uses grand piano key number to calculate frequency of the note
        self.frequency = 2 ** ((total_key - 46) / 12) * 440
        return self.frequency

    def interpolate_linearly(self, wave_table, index):
        """_summary_ generates sound into a wavetable given the premade table with values from 0-2pi

        Args:
            wave_table (numpy array): _description_ filled with values from 0-2pi
            index (float): _description_ where we are in the wavetable

        Returns:
            numpy array: _description_ wavetable with values we need to synthesize sound
        """
        # finds the indexes below and above the index
        truncated_index = int(np.floor(index))
        next_index = (truncated_index + 1) % wave_table.shape[0]

        # determines distance from each index
        next_index_weight = index - truncated_index
        truncated_index_weight = 1 - next_index_weight

        # interpolates indexes
        return truncated_index_weight * wave_table[truncated_index] + next_index_weight * wave_table[next_index]

    def fade_in_out(self, signal, fade_length):
        """_summary_ applies an amplitude envelope to the beginning and end of the sound so that the sound starts at an amplitude of 0 and we avoid any clicking
 
        Args:
            signal (numpy array): _description_ array containing the sound
            fade_length (int): _description_ duration of the fade in # of samples

        Returns:
            numpy array: _description_ finished sound
        """
        # builds the cosine envelope to dampen certain length of the signal
        fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
        fade_out = np.flip(fade_in)

        # applies envelope to the beginning and end of the signal
        signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
        signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length])

        # returns signal with fades applied
        return signal

    def square(self, x):
        """_summary_ logical representation of a square wave

        Args:
            x (int): _description_ index

        Returns:
            int: _description_ value of the function at input x
        """
        # generates a square function
        if math.sin(x) >= 0:
            return 1
        else: 
            return -1

    def triangle(self, x):
        """_summary_ mathematical representation of a triangle wave

        Args:
            x (int): _description_ index

        Returns:
            int: _description_ value of the function at input x
        """
        # generates a triangle function
        return (2 / np.pi) * abs(((x - (np.pi / 2)) % (2 * np.pi)) - np.pi) - 1

    def sawtooth(self, x):
        """_summary_ mathematical representation of a sawtooth wave

        Args:
            x (int): _description_ index

        Returns:
            int : _description_ value of the function at input x
        """
        # generates a sawtooth function
        return (x + np.pi) / np.pi % 2 - 1

    def synthesize(self):
        """_summary_ main function of this class, this is what actually synthesizes the sound
        """
        # preset parameters to achieve highest quality sound
        attack = 1000
        sample_rate = 44100
        wavetable_length = 64
        
        # sets the wave shape
        if self.waveform == 'Sine':
            waveform = np.sin
        elif self.waveform == 'Square':
            waveform = self.square
        elif self.waveform == 'Triangle':
            waveform = self.triangle
        elif self.waveform == 'Sawtooth':
            waveform = self.sawtooth

        # initializes the wavetable to encompass one whole period of the function
        wave_table = np.zeros((wavetable_length))
        for n in range(wavetable_length):
            wave_table[n] = waveform(2 * np.pi * n / wavetable_length)
        output = np.zeros((self.duration * sample_rate,))

        # determines the increment size in the table
        index = 0
        indexIncrement = self.frequency * wavetable_length / sample_rate

        # synthesizes the original sound
        for n in range(output.shape[0]):
            output[n] = self.interpolate_linearly(wave_table, index)
            index += indexIncrement
            index %= wavetable_length

        # sets the volume level based on the gain (original sound level is 0)
        amplitude = 10 ** (self.level / 20)
        output *= amplitude

        # applying fade to avoid clipping at beginning and end of signal
        output = self.fade_in_out(output, attack)

        # write the sound in a wav file
        wav.write(self.filename, sample_rate, output.astype(np.float32))

        # done
        return

    def playthis(self):        
        """_summary_ this method is what plays the sounds that are synthesized
        """
        # reads wav file
        self.sound = AudioSegment.from_wav(self.filename)

        # plays sound
        play(self.sound)

        #done
        return

# code used to generate premade files for real time mode (pre-generated a sound for ever key on the keyboard to reduce computing mode)

# octaves = [1,2,3,4,5,6,7]
# keys = [1,2,3,4,5,6,7,8,9,10,11,12]
# for i in range(0, len(octaves)):
#     for j in range(0, len(keys)):
#         note = Synthesizer(keys[j], 'Sine', octaves[i], -5, 1)
#         Synthesizer.synthesize(note)