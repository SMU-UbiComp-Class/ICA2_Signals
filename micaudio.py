__author__ = 'eclarson'

import pyaudio
import ringbuffer
import numpy as np

audio_data = ringbuffer.RingBuffer(100)


def audio_callback(in_data, frame_count, time_info, status):
    # define callback for PyAudio--this is called in separate thread
    global audio_data
    tmp = np.fromstring(in_data, dtype=np.int16)
    audio_data.insert_new(tmp)  # unpack the data, add to buffer
    return "", pyaudio.paContinue  # return nothing to play on speaker, and keep streaming


class MicAudio:
    """A class for sampling from the microphone"""

    def __init__(self, format_in=pyaudio.paInt16, channels=1, rate=44100, block_time=0.05, buffer_time=0.25):
        global audio_data
        # setup for the audio card
        self.format = format_in
        self.channels = channels
        self.rate = rate
        self.input_block_time = block_time
        self.input_frames_per_block = int(self.rate * self.input_block_time)
        self.buffer_time = buffer_time
        self.buffer_length_in_frames = int(self.rate * self.buffer_time)

        # instantiate PyAudio
        self.p = pyaudio.PyAudio()

        # setup the vector we will add audio samples to
        audio_data = ringbuffer.RingBuffer(self.buffer_length_in_frames)

        self.stream = None

    def start(self):
        # open stream using callback
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  frames_per_buffer=self.input_frames_per_block,
                                  input=True,
                                  stream_callback=audio_callback)

        # start the stream
        self.stream.start_stream()

    def stop(self):
        # stop stream
        self.stream.stop_stream()
        self.stream.close()

        # close PyAudio
        self.p.terminate()

    @staticmethod
    def get_samples():
        global audio_data
        tmp = audio_data.get_samples
        return tmp