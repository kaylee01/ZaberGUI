#from multiprocessing.connection import wait
from shutil import move
import PySimpleGUI as sg
from zaber_motion import Library, Units
from zaber_motion.ascii import Connection
from zaber_motion.ascii import Lockstep
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons
import pandas as pd
import sys
import glob
import serial
import icons

''' to do: deal with not integer inputs
make other ok button go on enter'''

Library.enable_device_db_store()

sg.theme('Reddit')

# max postions in mm
MAX_X = 151.49909375
MAX_Y = 151.49909375
MAX_Z = 40.000047

# initial move distance in mm
DIST = 15

# connection path (to be selected)
#SERIAL_PATH = "/dev/tty.usbmodem11301" # this is my one (remove at end)


# selecting the serial connection
# serial stuff here

#with Connection.open_serial_port("/dev/cu.usbmodem1101") as connection:

with Connection.open_serial_port(serial.SERIAL_PATH) as connection: #need to automate
    device_list = connection.detect_devices() 
    xy_device = device_list[0]
    z_device = device_list[1]

    axis1 = xy_device.get_axis(1)  # x
    axis2 = xy_device.get_axis(2)  # y
    axis3 = z_device.get_axis(1)   # z
    
    def is_in_bounds_r(axis, step):
        ''' checks if next step is in bounds '''
        if axis == axis1:   max = MAX_X
        if axis == axis2:   max = MAX_Y
        if axis == axis3:   max = MAX_Z
        
        current_pos = axis.get_position(Units.LENGTH_MILLIMETRES)
        if current_pos + step - max >= 0:
            return False
        return True

    def is_in_bounds_l(axis, step):
        ''' checks if next step is in bounds '''
        current_pos = axis.get_position(Units.LENGTH_MILLIMETRES)
        if current_pos - step >= 0:
            return True
        return False

    def move_right(axis, step):
        ''' moves the specified axis to the right by the step amount '''

        if axis == axis1:   max, coord = MAX_X, "x"
        if axis == axis2:   max, coord = MAX_Y, "y"
        if axis == axis3:   max, coord = MAX_Z, "z"
        
        if (is_in_bounds_r(axis, step)):
            axis.move_relative(step, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        else:
            axis.move_absolute(max, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
            sg.popup_no_wait("You are at max {} position".format(coord), title="max", button_color=("White", "Red"))
            

    def move_left(axis, step):
        ''' moves the specified axis to the left by the step amount '''

        if axis == axis1:   max, coord = MAX_X, "x"
        if axis == axis2:   max, coord = MAX_Y, "y"
        if axis == axis3:   max, coord = MAX_Z, "z"

        if is_in_bounds_l(axis, step):
            axis.move_relative(-step, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        else:
            axis.move_absolute(0)
            sg.popup_no_wait("You are at min {} position".format(coord), title="max", button_color=("White", "Red"))
                
    def move_small_end(axis):
        ''' if the axis is closer than a 'step' distance away from the small edge, it will be moved to the edge using this function '''
        if axis == axis1:   coord = "x"
        if axis == axis2:   coord = "y"
        if axis == axis3:   coord = "z"

        if axis.get_position(Units.LENGTH_MILLIMETRES) != 0:
            axis.move_absolute(0, wait_until_idle=False)
        else:
            sg.popup_no_wait("You are at min {} position".format(coord), title="max", button_color=("White", "Red"))

    def move_big_end(axis):
        ''' if the axis is closer than a 'step' distance away from the far edge, it will be moved to the edge using this function '''
        if axis == axis1:   max, coord = MAX_X, "x"
        if axis == axis2:   max, coord = MAX_Y, "y"
        if axis == axis3:   max, coord = MAX_Z, "z"

        if axis.get_position(Units.LENGTH_MILLIMETRES) != max:
            axis.move_absolute(max, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        else:
            sg.popup_no_wait("You are at max {} position".format(coord), title="max", button_color=("White", "Red"))


        axis1.move_absolute(MAX_X, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
    
    def move_to_abs(x, y, z):
        ''' Moves to specified absolute positon. If an input is invalid, it will be ignored and other valid movements will occur '''
        if x != "":
            try:
                if float(x) < 0 or float(x) > MAX_X:
                    sg.popup_no_wait("Please enter a valid X postion.\n X: (0 to 151.49) mm", title="X error", button_color=("White", "Red"))
                else:
                    axis1.move_absolute(float(values["-INX-"]), Units.LENGTH_MILLIMETRES, wait_until_idle=False)

            except:
                sg.popup_no_wait("Please enter a valid X postion.\n X: (0 to 151.49) mm", title="X error", button_color=("White", "Red"))

        if y != "":
            try:
                if float(y) < 0 or float(y) > MAX_Y:
                    sg.popup_no_wait("Please enter a valid Y postion.\n Y: (0 to 151.49) mm", title = "Y error", button_color = ("White", "Red"))
                else: 
                    axis2.move_absolute(float(values["-INY-"]), Units.LENGTH_MILLIMETRES, wait_until_idle=False)

            except:
                sg.popup_no_wait("Please enter a valid Y postion.\n Y: (0 to 151.49) mm", title = "Y error", button_color = ("White", "Red"))
                

        if z != "":
            try:
                if float(z) < 0 or float(z) > MAX_Z:
                    sg.popup_no_wait("Please enter a valid Z postion.\n Z: (0 to 40.00) mm", title = "Z error", button_color = ("White", "Red"))
                else: 
                    axis3.move_absolute(float(values["-INZ-"]), Units.LENGTH_MILLIMETRES, wait_until_idle=False)

            except:
                sg.popup_no_wait("Please enter a valid Z postion.\n Z: (0 to 40.00) mm", title = "Z error", button_color = ("White", "Red"))

    def move_rel(x,y,z):
        ''' moves the platform by the inputted amounts '''
        if x != "":
            try:
                if float(x) < 0:
                    move_left(axis1, abs(float(x)))
                else:
                    move_right(axis1, float(x))

            except:
                sg.popup_no_wait("Please enter a valid X postion.\n X: (0 to 151.49) mm", title="X error", button_color=("White", "Red"))

        if y != "":
            try:
                if float(y) < 0:
                    move_left(axis2, abs(float(y)))
                else:
                    move_right(axis2, float(y))

            except:
                sg.popup_no_wait("Please enter a valid Y postion.\n X: (0 to 151.49) mm", title="Y error", button_color=("White", "Red"))
 

        if z != "":
            try:
                if float(z) < 0:
                    move_left(axis3, abs(float(z)))
                else:
                    move_right(axis3, float(z))

            except:
                sg.popup_no_wait("Please enter a valid Z postion.\n Z: (0 to 40.00) mm", title = "Z error", button_color = ("White", "Red"))


    def set_step(step):
        ''' change step size to inputted value'''
        try:
            if float(step) >= 0:
                global DIST 
                DIST = float(step)
                window["-mm-"].update("{} mm".format(DIST))
            else:
                sg.popup("Please enter a valid step size.", title="Step size error", button_color=("White", "Red"))
        except:
            sg.popup("Please enter a valid step size.", title="Step size error", button_color=("White", "Red"))

    def centre():
        ''' moves platfrom to the centre '''
        axis1.move_absolute(MAX_X/2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        axis2.move_absolute(MAX_Y/2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        axis3.move_absolute(MAX_Z/2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)


# PLOTTER (make try and except function to account for errors. Maybe make it look for t column etc.)
    def load_csv(csv_path):
        ''' the inputted csv file must have columns t,x,y,z in this order for this to work '''
        df = pd.read_csv(csv_path)
        t = df["t"]
        maxt = len(t)-1
        x = df["x"]
        y = df["y"]
        z = df["z"]

        return t,x,y,z, maxt

    def plotter(x,y,z,t):
        ''' plots to graphs in the window. The bottom plot is an interactive 3d representation of the tumour movement'''
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
        ax2.set_xlabel('time (s)')
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


    col2 = [
        [sg.Button('', image_data=icons.Uparrow.base64,button_color=('white', 'white'), pad=(0,0), key='-ZREND-')],
        [sg.Button('', image_data=icons.uparrow.base64,button_color=('white', 'white'), pad=(0,0), key='-ZRIGHT-')],
        [sg.Text('Z', font = 'Any 16')],
        [sg.Button('', image_data=icons.downarrow.base64,button_color=('white', 'white'), pad=(0,0), key='-ZLEFT-')],
        [sg.Button('', image_data=icons.Downarrow.base64,button_color=('white', 'white'), pad=(0,0), key='-ZLEND-')],
    ]

    col_buffer = [
        [sg.Text('', size=(10,20))],
    ]

    col1 = [
        #[sg.Text('Column1', background_color='red', size=(20,20))],
        [
            sg.Button('', image_data=icons.Up.base64,button_color=('white', 'white'), pad=(0,0), key='-YREND-'),
        ],
        [
            sg.Button('', image_data=icons.up.base64,button_color=('white', 'white'), pad=(0,0), key='-YRIGHT-'),
        ],
        [
            #sg.Button("End", key="-XLEND-"), 
            sg.Button('', image_data=icons.Left.base64, button_color=('white', 'white'), pad=(0,0), key='-XLEND-'),
            #sg.Button(" Left ", key="-XLEFT-"), 
            sg.Button('', image_data=icons.left.base64, button_color=('white', 'white'), pad=(0,0), key='-XLEFT-'),
            #sg.Text("            ", font='Any 16'),
            sg.Button('', image_data=icons.axis.base64, button_color=('white', 'white'), pad=(0,0), size=(1,1)),
            #sg.Button("Right", key="-XRIGHT-"),
            sg.Button('', image_data=icons.right.base64,button_color=('white', 'white'), pad=(0,0), key='-XRIGHT-'), 
            #sg.Button("End", key="-XREND-"),
            sg.Button('', image_data=icons.Right.base64,button_color=('white', 'white'), pad=(0,0), key='-XREND-'), 
            #sg.Column(col_layout)
        ],
        [
            
            #sg.Button("Right", key="-YRIGHT-"),
            sg.Button('', image_data=icons.down.base64,button_color=('white', 'white'), pad=(0,0), key='-YLEFT-'),
            #sg.Button("End", key="-YREND-"),  
        ],
        [
            sg.Button('', image_data=icons.Down.base64,button_color=('white', 'white'), pad=(0,0), key='-YLEND-'), 
        ],
    ]
        
        
        
    layout = [
        [
            #sg.Button("STOP pls", key="-STOP-", )
            # change stop64 to icons.stop.base64
            sg.Button('', image_data=icons.stop.base64,button_color=('white', 'white'), pad=(0,0), key='-STOP-'),
            sg.Button('', image_data=icons.home.base64,button_color=('white', 'white'), pad=(0,0), key='-HOME-'),
            sg.Button('', image_data=icons.centre.base64,button_color=('white', 'white'), pad=(0,0), key='-CENTRE-'),
        ],

        [sg.HorizontalSeparator(color='#2084d8')],

        [
            sg.Text("X position:", font = 'Any 16'),
            sg.Text("{:.2f} mm".format(axis1.get_position(Units.LENGTH_MILLIMETRES)),key="-CURRENTX-", font = 'Any 16')
        ], 
        [
            sg.Text("Y position:", font = 'Any 16'),
            sg.Text("{:.2f} mm".format(axis2.get_position(Units.LENGTH_MILLIMETRES)),key="-CURRENTY-", font = 'Any 16')
        ],
        [
            sg.Text("Z position:", font = 'Any 16'),
            sg.Text("{:.2f} mm".format(axis3.get_position(Units.LENGTH_MILLIMETRES)),key="-CURRENTZ-", font = 'Any 16')
        ],
        [   
            sg.Text("Set step size:", font='Any 16'),
            sg.InputText(key="-STEP-", size=(5,1)),
            sg.Text("{} mm".format(DIST), key="-mm-", font='Any 16'), 
            sg.Button("OK", key="-OK-", bind_return_key=True),
            #sg.Button('', image_data=tick164,button_color=('white', 'white'), pad=(0,0), key='-OK-'),
        ],
        [sg.Column(col1, element_justification='c' ), sg.Column(col_buffer), sg.Column(col2, element_justification='c' )],
        [
            sg.Text("Relative movements (x,y,z):         ", font = 'Any 16'), 
            sg.InputText(key='-INXRel-', size=(3,1)), 
            sg.InputText(key='-INYRel-', size=(3,1)), 
            sg.InputText(key='-INZRel-', size=(3,1)),
            sg.Button("OK", key="-OK2-", bind_return_key=True)
        ],
        [
            sg.Text("Move to absolute position (x,y,z):", font = 'Any 16'), 
            sg.InputText(key='-INX-', size=(3,1)), 
            sg.InputText(key='-INY-', size=(3,1)), 
            sg.InputText(key='-INZ-', size=(3,1)),
            sg.Button("OK", key="-OK1-", bind_return_key=True)
        ],
    ]

    plot=[
        [
            sg.Text('Select csv file', font = 'Any 16',),
            sg.Input(), 
            sg.FileBrowse('FileBrowse', file_types=(("CSV files", "*.csv"),)), 
            sg.Button("Display", key="-FILE-")
        ],
    ]

    tabgrp = [
    [sg.TabGroup([[sg.Tab('Movement', layout, element_justification= 'center'),
                    sg.Tab('Modelling', plot,),
                    ]], tab_location='centertop',
                        border_width=1)]
        ]  

    window = sg.Window('Zaber GUI', tabgrp, size = (750,750), element_justification='c')

    # start of event loop
    while True:
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-XLEND-":
            move_small_end(axis1)

        if event == "-XRIGHT-":
            move_right(axis1, DIST)

        if event == "-XLEFT-":
            move_left(axis1, DIST)

        if event == "-XREND-":
            move_big_end(axis1)

        #####################

        if event == "-YLEND-":
            move_small_end(axis2)
            
        if event == "-YRIGHT-":
            move_right(axis2, DIST)

        if event == "-YLEFT-":
            move_left(axis2, DIST)

        if event == "-YREND-":
            move_big_end(axis2)

        #####################
        
        if event == "-ZLEND-":
            move_small_end(axis3)

        if event == "-ZRIGHT-":
            move_right(axis3, DIST)

        if event == "-ZLEFT-":
            move_left(axis3, DIST)

        if event == "-ZREND-":
            move_big_end(axis3)


        ####################
        
        if event == "-HOME-":
            connection.home_all(wait_until_idle=False)
        
        if event == "-CENTRE-":
            centre()

        if event == "-OK-":
            set_step(values['-STEP-'])
            window["-STEP-"].update("")

        if event == "-OK1-":
            move_to_abs(values['-INX-'], values['-INY-'], values['-INZ-'])
            window["-INX-"].update("")
            window["-INY-"].update("")
            window["-INZ-"].update("")

        if event == "-STOP-":
            connection.stop_all()

        if event == "-OK2-":
            move_rel(values["-INXRel-"], values["-INYRel-"], values["-INZRel-"])
            #window["-INXRel-"].update("")
            #window["-INYRel-"].update("")
            #window["-INZRel-"].update("")
        
        if event == "-FILE-":
            pathname = values['FileBrowse']
            if pathname.lower().endswith((".csv")):
                display(pathname)
            else:
                sg.popup_no_wait("Only CSV file types are supported.", title="max", button_color=("White", "Red"))

                


        #axis1.wait_until_idle()
        #axis2.wait_until_idle()
        #axis3.wait_until_idle()
            
        # note : these only update directly after action when axis is set to idle. However, when set to idle, stop button will not work
   
        window["-CURRENTX-"].update("{:.2f} mm".format(axis1.get_position(Units.LENGTH_MILLIMETRES)))
        window["-CURRENTY-"].update("{:.2f} mm".format(axis2.get_position(Units.LENGTH_MILLIMETRES)))
        window["-CURRENTZ-"].update("{:.2f} mm".format(axis3.get_position(Units.LENGTH_MILLIMETRES)))