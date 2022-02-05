'''
Written by Kaylee Molin (22734429) 2/2/22
Popup screen where youcan select the serail connection for the zaber platform
'''

import os 
import PySimpleGUI as sg
import glob

sg.theme('Reddit')
SERIAL_PATH = ''
test_list = ["hi", "kaylee", "this", "is", "a", "list", "stupid"]

#input("Make sure device is removed, then press a key...") 
b4 = os.listdir("/dev") 
#input("Now plug in the device, then hit any key...") 
after = os.listdir("/dev") 
#print("Newly plugged in devices:\n") 
for line in after: 
    if line not in b4: 
        #print(line)
        SERIAL_PATH = line

def get_connections():
    tty = glob.glob('/dev/tty*')
    cu = glob.glob('/dev/cu*')
    return tty + cu

# selecting the serial connection
layoutSerial = [
    [sg.Text('Select serial/USB connection:', font = 'Any 16')],
    [sg.Combo(get_connections(), size=(40,10), font = 'Any 16', enable_events=False, key='-CONNECTIONS-')],
    [sg.Button('OK', key='-OKSERIAL-'), sg.Exit()]
          ]

window = sg.Window('Window Title', layoutSerial)    



while True:
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == '-OKSERIAL-':
            SERIAL_PATH = values['-CONNECTIONS-']
            print(SERIAL_PATH)
            window.close()