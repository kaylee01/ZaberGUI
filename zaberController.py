''' 
Written by Kaylee Molin (22734429) 
01/12/21
'''

from zaber_motion import Library, Units
from zaber_motion.ascii import Connection

Library.enable_device_db_store()

# https://www.zaber.com/software/docs/motion-library/ascii/tutorials/initialize/


#ser = BinarySerial("/dev/cu.usbmodem1101")

import sys
import glob
import serial


#print(glob.glob('/dev/tty.*')) # prints ports
# need to try automate this in the future


with Connection.open_serial_port("/dev/cu.usbmodem1101") as connection:
    device_list = connection.detect_devices() 
    print("Found {} devices".format(len(device_list)))

    # The rest of your program goes here (indented)

    xy_device = device_list[0]
    #print ("\n #### {} #### \n".format(xy_device))
    z_device = device_list[1]
    #print ("\n #### {} #### \n".format(z_device))

    # homes the device
    axis1 = xy_device.get_axis(1) # x ?
    print ("\n #### {} #### \n".format(axis1))
    axis2 = xy_device.get_axis(2) # y ?
    print ("\n #### {} #### \n".format(axis2))
    axis3 = z_device.get_axis(1)
    print ("\n #### {} #### \n".format(axis3))
    #axis1.home()
    #axis2.home()
    #axis3.home()

    #axis1.move_absolute(40, Units.LENGTH_MILLIMETRES)

    def home_all():
        for device in device_list:
            print("Homing all axes of device with address {}.".format(device.device_address))
            device.all_axes.home()
    

    ''' Move to specified location in mm'''
    def move_to_pos(x,y,z):
        axis1.move_absolute(x, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        axis2.move_absolute(y, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        axis3.move_absolute(z, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        
        axis1.wait_until_idle()
        axis2.wait_until_idle()
        axis3.wait_until_idle()

    def main():
        #home_all()
        #move_abs("ds", 5)
        #move_abs(axis3, 40)
        #move_abs(axis1, 40)
        #move_abs(axis2, 40)

        #move_to_pos(0,0,0)
        #move_to_pos(5,5,5)
        #axis3.move_max()
        print("xX " + str(axis3.get_position(Units.LENGTH_MILLIMETRES)))

        #axis1.move_velocity(-400, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        move_to_pos(10,10,10)
        #home_all()


        #axis1.move_absolute(10000)
        #axis2.move_relative(10000)
        #axis3.move_relative(10000)
    
    main()
