'''
Written by Kaylee Molin (22734429) 2/2/22
Popup screen where you can select the serial connection for the zaber platform
'''

import os 
import PySimpleGUI as sg
import glob
import time

sg.theme('Reddit')
SERIAL_PATH = ''


def get_new_connections():
    input("Make sure device is removed, then press a key...") 
    before = os.listdir("/dev") 
    input("Now plug in the device, then hit any key...") 
    after = os.listdir("/dev") 
    print("Newly plugged in devices:\n") 
    for line in after: 
        if line not in before: 
            print(line)
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

layoutSerial2 = [
    [sg.Text('Make sure the device is unplugged then click \'OK\'', key='-TEXT-',font = 'Any 16')],
    #[sg.Text('Alternatively, select the device from the list below if the connection port is alreadt known', key='-TEXT2-',font = 'Any 16')],
    [sg.Combo(SERIAL_PATH, size=(40,10), font = 'Any 16', enable_events=False, key='-CONNECTIONS-')],
    [sg.Button('OK', key='-OKSERIAL-'), sg.Exit()]
          ]

window = sg.Window('Serial Connection', layoutSerial2)    

ok_count = 0
connection_list = []

while True:
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == '-OKSERIAL-':
            ok_count += 1
            SERIAL_PATH = values['-CONNECTIONS-']
            print(SERIAL_PATH)
            
            if ok_count == 1:
                window["-TEXT-"].update("Now plug in your device and click \'OK\'.")
                time.sleep(1)
                before = os.listdir("/dev") 
                
            
            if ok_count == 2:
                window["-TEXT-"].update("Select your device from the dropdown menu.")
                time.sleep(1)
                after = os.listdir("/dev") 
                
                for line in after: 
                    if line not in before and line.startswith('cu'): 
                        print(line)
                        #SERIAL_PATH = line
                        connection_list.append(line)
                window['-CONNECTIONS-'].update(value='', values=connection_list)
                
            if ok_count == 3:
                SERIAL_PATH = "/dev/" + values['-CONNECTIONS-']
                print("...." + SERIAL_PATH)
                window.close()
                


            

            