import numpy as np
import matplotlib

matplotlib.use('TKAgg')  # need to use this on OSX for animate w/ blit=True

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D
import micaudio

audio = micaudio.MicAudio()
FFT_SIZE = audio.buffer_length_in_frames

# setup the figure to plot with
fig = plt.figure()

# setup the time plot
ax1 = fig.add_subplot(2, 1, 1)
ax1.set_xlim(0, float(audio.buffer_length_in_frames) / audio.rate)
ax1.set_ylim(-2000, 2000)
line1 = Line2D([], [], color='red', linewidth=0.5)
ax1.add_line(line1)

#setup the frequency plot
ax2 = fig.add_subplot(2, 1, 2)
ax2.set_xlim(0, audio.rate)
ax2.set_ylim(-50, 100)
line2 = Line2D([], [], color='blue', linewidth=0.5)
ax2.add_line(line2)


# initialization, plot nothing (this is also called on resize)
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2


# animation function.  This is called sequentially, after calling plt.show() (on main thread)
def animate(i):
    # get the audio samples from the buffer
    x = np.linspace(0, audio.buffer_time, audio.buffer_length_in_frames)
    y = audio.get_samples()
    line1.set_data(x, y)

    # now take the FFT of the data
    y_fft = 20*np.log10(np.abs(np.fft.rfft(y, FFT_SIZE)))
    freq = np.linspace(0, audio.rate, len(y_fft))
    print (np.argmax(y_fft))
    line2.set_data(freq, y_fft)
    return line1, line2

audio.start()

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

# this is a blocking call that will sequentially call the animate function
# the pyaudio thread will keep running and update the buffer of samples
plt.show()

audio.stop()