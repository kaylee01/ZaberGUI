import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


df = pd.read_csv('/Users/kayleemolin/Desktop/summer_project/ZaberGUI/movementData.csv')

t = df["t"]
x = df["x"]
minx=min(x)
maxx=max(x)

y = df["y"]
miny=min(y)
maxy=max(y)

z = df["z"]
minz=min(z)
maxz=max(z)

init_i = 0

# Create the figure and the line that we will manipulate
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#fig, ax = plt.subplots()
#line, = plt.plot(x[init_i],y[init_i],z[init_i], "bo")

mylines=ax.plot(x[init_i],y[init_i],z[init_i], "bo")

plt.plot(x,y,z, alpha=0.1)
#ax.set_xlim(minx,maxx)
#ax.set_ylim(miny,maxy)
ax.set_xlabel('x position')
ax.set_ylabel('y position')
ax.set_zlabel('z position')


# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.15, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = plt.axes([0.15, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Time',
    valmin=0,
    valmax=2500,
    valinit=init_i,
    valstep=1
)

# The function to be called anytime a slider's value changes
def update(val):
    #line.set_ydata(f(t, amp_slider.val, freq_slider.val))
    '''line.set_xdata(x[val])
    line.set_ydata(y[val])
    #line.set_zdata(z[val])

    line.set_3d_properties(z[val])'''

    mylines[0].set_xdata(x[val])
    mylines[0].set_ydata(x[val])
    mylines[0].set_3d_properties(z[val])
    
    fig.canvas.draw_idle()


# register the update function with each slider
freq_slider.on_changed(update)
#amp_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    freq_slider.reset()
button.on_clicked(reset)

plt.show()