'''
Written by Kaylee Molin 21/01/2022

Plots the position of a tumour in the x, y and z plane. Slider for time.
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons
import pandas as pd

def load_csv(csv_path):
    df = pd.read_csv(csv_path)
    t = df["t"]
    maxt = len(t)-1
    x = df["x"]
    y = df["y"]
    z = df["z"]

    return t,x,y,z, maxt

def plotter(x,y,z,t):
    #fig = plt.subplot(2, 1, 1)
    fig = plt.figure(figsize=(8, 8))    # window size
    plt.subplots_adjust(bottom=0.25) 
    
    ax = fig.add_subplot(212, projection='3d') 
    ax.set_xlabel('x position (mm)')
    ax.set_ylabel('y position (mm)')
    ax.set_zlabel('z position (mm)')

    l=ax.plot(x[0],y[0],z[0], "bo")
    ax.plot(x,y,z, alpha=0.2)

    ax2 = fig.add_subplot(211)
    ax2.set_xlabel('time')
    ax2.set_ylabel('displacement (mm)')
    ax2.plot(t, x, label='x')
    ax2.plot(t, y, label='y')
    ax2.plot(t, z, label='z')
    ax2.legend()

    return plt, fig, ax


def create_slider(plt,fig,ax,maxt):

    # Make a horizontal slider to control the time.
    axtime = plt.axes([0.15, 0.1, 0.65, 0.03])
    freq_slider = Slider(
        ax=axtime,
        label='Time',
        valmin=0,
        valmax=maxt,
        valinit=0,
        valstep=1,
    )

    return freq_slider

def display(filename):
    t,x,y,z,maxt = load_csv(filename)

    plt, fig, ax = plotter(x,y,z,t)
    freq_slider = create_slider(plt,fig,ax,maxt)

    def update(val): 
        h = freq_slider.val 
        ax.clear()
        l=ax.plot(x[h],y[h],z[h], "bo")
        ax.plot(x,y,z, alpha=0.2)
        ax.set_xlabel('x position (mm)')
        ax.set_ylabel('y position (mm)')
        ax.set_zlabel('z position (mm)')
        
        fig.canvas.draw_idle()
        
    freq_slider.on_changed(update)

    plt.show()

display('/Users/kayleemolin/Desktop/summer_project/ZaberGUI/movementData.csv')
#display('/Users/kayleemolin/Desktop/summer_project/ZaberGUI/movementData2.csv')