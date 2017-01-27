import numpy as np
import matplotlib
matplotlib.use('TKAgg')  # need to use this on OSX for animate w/ blit=True
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D

# setup the figure to plot with
fig = plt.figure()

# setup the plot
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_xlim(0, 1)
ax1.set_ylim(-1, 1)
line1 = Line2D([], [], color='red', linewidth=0.5)
ax1.add_line(line1)


# initialization, plot nothing (this is also called on resize)
def init():
    # called on first plot or redraw
    line1.set_data([], [])  # just draw blank background
    return line1,


# animation function.  This is called sequentially, after calling plt.show() (on main thread)
def animate(i):
    # generate some data to draw
    x = np.linspace(0, 2, 100)
    y = np.sin(2*np.pi*(x + i*0.02))
    line1.set_data(x, y)

    # return line(s) to be drawn
    return line1,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig,  # the figure to use
                               animate,  # the function to call
                               init_func=init,  # the function to init the drawing with
                               frames=200,  # the max value of "i" in the animate function, before resetting
                               interval=20,  # 20 ms between each call
                               blit=True)  # do not redraw anything that stays the same between animations

# this is a blocking call that will sequentially call the animate function
plt.show()

