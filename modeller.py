import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import genfromtxt

df = pd.read_csv('/Users/kayleemolin/Desktop/summer_project/ZaberGUI/movementData.csv')

t = df["t"]
x = df["x"]
y = df["y"]
z = df["z"]
xy = df[["x","y"]]

def simple_plot():
    plt.plot(t, x, label='x position')
    plt.plot(t, y, label='y position')
    plt.plot(t, z, label='z position')
    plt.xlabel("Time (s)")
    plt.ylabel("Movement (mm)")
    
    plt.legend()
    plt.show()
    
def xy_plot():
    plt.plot(x,y)
    plt.xlabel("x")
    plt.ylabel("x")
    plt.show()
    
def xz_plot():
    plt.plot(x,z)
    plt.show()
    
def yz_plot():
    plt.plot(y,z)
    plt.show()
    
xy_plot()
xz_plot()
yz_plot()