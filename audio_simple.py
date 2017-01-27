import numpy as np
import micaudio  # you must have pyaudio installed for this
import time

# setup audio with default parameters
audio = micaudio.MicAudio()

# start firing off and saving samples from audio card
audio.start()  # this is a non-blocking call

while True:
    # get the most recent audio samples from buffer
    y = audio.get_samples()  # this returns a numpy vector of audio samples

    # do something with these numbers
    print(np.max(y))
    time.sleep(0.25)

audio.stop()  # be sure to shutdown the audio card