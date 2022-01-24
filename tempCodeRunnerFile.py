ax = fig.add_subplot(121, projection='3d')        
X= np.arange(-50,50,2)
Y=np.arange(-50,50,2)
X,Y = np.meshgrid(X,Y)

Z = np.sqrt((X**2+Y**2)/(np.tan(np.pi/120)))            
ax.plot_wireframe(X,Y,Z, rstride=3, cstride=3)  