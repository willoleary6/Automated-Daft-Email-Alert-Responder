import os
import sys
import time


def _is_connected_to_emulator(arr_response):
    for line in arr_response:
        if line.startswith('localhost:5555'):
            return True
    return False


def main():
    os.chdir('C:\\adb\\platform-tools')  # This will change the present working directory
    connected_devices = os.popen('adb devices -l').read().split('\n')  # get list of connected devices

    connected_to_emulator = _is_connected_to_emulator(connected_devices)

    if not connected_to_emulator:
        os.popen('adb connect localhost:5555').read()
        connected_devices = os.popen('adb devices -l').read().split('\n')
        connected_to_emulator = _is_connected_to_emulator(connected_devices)
        if not connected_to_emulator:
            print("cant connect to emulator")
            # TODO look into spooling up bluestacks automatically
            sys.exit()
    # list all the applications on the emulator
    # list_of_applications_on_emulator = os.popen('adb -s localhost:5555 shell pm list packages -f').read()
    # print(list_of_applications_on_emulator)

    # opening gmail
    os.popen('adb -s localhost:5555 shell monkey -p com.google.android.gm -v 1').read()
    time.sleep(3)
    os.popen('adb -s localhost:5555 shell input touchscreen tap 200 100').read()  # open folders
    time.sleep(1)
    # swipe the options to bring the inFocus
    os.popen('adb -s localhost:5555 shell input touchscreen swipe 200 1000 200 400 ').read()
    time.sleep(1)
    # tap inFocus label
    os.popen('adb -s localhost:5555 shell input touchscreen tap 200 600 ').read()
    time.sleep(1)
    # close the folder button
    os.popen('adb -s localhost:5555 shell input touchscreen tap 500 100 ').read()
    time.sleep(1)
    # open daft ad
    os.popen('adb -s localhost:5555 shell input touchscreen tap 1000 1000 ').read()

    # TODO also need to look into closing gmail and daft after im done with them
'''
input touchscreen tap 200 600 # tap inFocus label

input touchscreen tap 500 100 # close the folder button

input touchscreen tap 1000 1000 # open daft ad
'''

if __name__ == '__main__':
    main()
