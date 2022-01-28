'''
Written by Kaylee Molin 21/01/2022

Plots the position of a tumour in the x, y and z plane. Slider for time.
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons
import pandas as pd

df = pd.read_csv('/Users/kayleemolin/Desktop/summer_project/ZaberGUI/movementData.csv')

t = df["t"]
x = df["x"]
y = df["y"]
z = df["z"]

init_i = 0


fig = plt.figure()
plt.subplots_adjust(bottom=0.25) 


ax = fig.add_subplot(111, projection='3d') 
ax.set_xlabel('x position')
ax.set_ylabel('y position')
ax.set_zlabel('z position')

l=ax.plot(x[0],y[0],z[0], "bo")
ax.plot(x,y,z, alpha=0.2)

# Make a horizontal slider to control the time.
axtime = plt.axes([0.15, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axtime,
    label='Time',
    valmin=0,
    valmax=2500,
    valinit=0,
    valstep=1
)

def update(val): 
    h = freq_slider.val 
    ax.clear()
    l=ax.plot(x[h],y[h],z[h], "bo")
    ax.plot(x,y,z, alpha=0.2)
    ax.set_xlabel('x position')
    ax.set_ylabel('y position')
    ax.set_zlabel('z position')
    

    fig.canvas.draw_idle() 
freq_slider.on_changed(update)

plt.show()