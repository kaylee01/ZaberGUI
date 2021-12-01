from zaber_motion import Library
from zaber_motion.ascii import Connection

Library.enable_device_db_store()

# https://www.zaber.com/software/docs/motion-library/ascii/tutorials/initialize/


#ser = BinarySerial("/dev/cu.usbmodem1101")

import sys
import glob
import serial


print(glob.glob('/dev/tty.*')) # prints ports
# need to try automate this in the future


with Connection.open_serial_port("/dev/cu.usbmodem1101") as connection:
    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))

    # The rest of your program goes here (indented)
    