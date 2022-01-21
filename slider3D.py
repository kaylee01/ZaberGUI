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
        
'''ax = fig.add_subplot(121, projection='3d')        
X= np.arange(-50,50,2)
Y=np.arange(-50,50,2)
X,Y = np.meshgrid(X,Y)

Z = np.sqrt((X**2+Y**2)/(np.tan(np.pi/120)))            
ax.plot_wireframe(X,Y,Z, rstride=3, cstride=3)  '''       
#plt.axis('scaled')

h0=0

ax2 = fig.add_subplot(111, projection='3d') 

#Z2 = 0*X+0*Y+h0        

#l=ax2.plot_surface(X,Y,Z2,color='red',rstride=2, cstride=2)
l=ax2.plot(x[init_i],y[init_i],z[init_i], "bo")
ax2.plot(x,y,z, alpha=0.1)
'''axhauteur = plt.axes([0.2, 0.1, 0.65, 0.03])
shauteur = Slider(axhauteur, 'Hauteur', 0.5, 10.0, valinit=h0)
'''



# Make a horizontal slider to control the time.
axtime = plt.axes([0.15, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axtime,
    label='Time',
    valmin=0,
    valmax=2500,
    valinit=init_i,
    valstep=1
)

def update(val): 
    h = freq_slider.val 
    ax2.clear()
    #l=ax2.plot_surface(X,Y,0*X+0*Y+h,color='red',rstride=2, cstride=2)
    l=ax2.plot(x[h],y[h],z[h], "bo")
    ax2.plot(x,y,z, alpha=0.1)
    ax2.set_xlim(min(x),max(x))
    ax2.set_ylim(min(y),max(y))
    ax2.set_zlim(min(z),max(z))
    fig.canvas.draw_idle() 
freq_slider.on_changed(update)
#ax2.set_zlim(0,10)

plt.show()