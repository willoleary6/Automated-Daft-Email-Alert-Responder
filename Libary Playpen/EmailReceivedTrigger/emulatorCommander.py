import os
import sys
import time
import subprocess


def _is_connected_to_emulator(arr_response):
    for line in arr_response:
        if line.startswith('localhost:5555'):
            return True
    return False


def _write_message(message):
    use_phone_number = True
    phone_number = '0834740410'
    # leaving option open as scam listings may be present
    if use_phone_number:
        time.sleep(3)
        os.popen('adb -s localhost:5555 shell input touchscreen tap 250 730').read()
        time.sleep(3)
        os.popen('adb -s localhost:5555 shell input text "' + phone_number + '"').read()

    # open the text box
    time.sleep(3)
    os.popen('adb -s localhost:5555 shell input touchscreen tap 100 900').read()

    lines = message.split("\n")
    for l in lines:
        time.sleep(3)
        os.popen('adb -s localhost:5555 shell input text "' + l.strip().replace(" ", "\ ") + '"').read()
        time.sleep(1)
        os.popen('adb -s localhost:5555 shell input keyevent "KEYCODE_ENTER"').read()


def _navigate_to_add_listing():
    # opening gmail
    os.popen('adb -s localhost:5555 shell monkey -p com.google.android.gm -v 1').read()
    time.sleep(10)
    os.popen('adb -s localhost:5555 shell input touchscreen tap 200 100').read()  # open folders
    time.sleep(3)
    # swipe the options to bring the inFocus
    os.popen('adb -s localhost:5555 shell input touchscreen swipe 200 1000 200 400 ').read()
    time.sleep(3)
    # tap inFocus label
    os.popen('adb -s localhost:5555 shell input touchscreen tap 200 600 ').read()
    time.sleep(3)
    # close the folder button
    os.popen('adb -s localhost:5555 shell input touchscreen tap 500 100 ').read()
    time.sleep(3)
    # open daft ad
    os.popen('adb -s localhost:5555 shell input touchscreen tap 1000 1000 ').read()
    # open the messaging screen
    time.sleep(10)
    os.popen('adb -s localhost:5555 shell input touchscreen tap 500 1850').read()


def _close_down_apps():
    time.sleep(3)
    os.popen('adb -s localhost:5555 shell am force-stop com.google.android.gm').read()
    time.sleep(10)
    os.popen('adb -s localhost:5555 shell am force-stop com.daft.ie').read()
    # ensuring the first app closed stays closed
    time.sleep(3)
    os.popen('adb -s localhost:5555 shell am force-stop com.google.android.gm').read()


def _spool_up_emulator(failed_attempts=0):
    if failed_attempts < 3:
        os.popen('adb connect localhost:5555').read()
        connected_devices = os.popen('adb devices -l').read().split('\n')
        connected_to_emulator = _is_connected_to_emulator(connected_devices)
        if not connected_to_emulator:
            # emulator is not running, create a new instance
            subprocess.Popen(['C:\ProgramData\BlueStacks\Client\Bluestacks.exe'])
            time.sleep(210)  # wait 3.5 minutes for blue stacks to spool up
            _spool_up_emulator(failed_attempts + 1)
    else:
        print("cant connect to emulator")
        sys.exit()


def message_landlord_on_emulator(message):
    os.chdir('C:\\adb\\platform-tools')  # This will change the present working directory
    connected_devices = os.popen('adb devices -l').read().split('\n')  # get list of connected devices

    connected_to_emulator = _is_connected_to_emulator(connected_devices)

    if not connected_to_emulator:
        _spool_up_emulator()

    _navigate_to_add_listing()

    # write message
    _write_message(message)

    # terms and conditions
    # time.sleep(2) # blocking the terms and conditions checkbox so I don't spam people
    # os.popen('adb -s localhost:5555 shell input touchscreen tap 55 1100').read()

    # hit send message button
    time.sleep(3)
    os.popen('adb -s localhost:5555 shell input touchscreen tap 550 1190').read()

    _close_down_apps()


if __name__ == '__main__':
    message_landlord_on_emulator("Hi, \n is this property still available? \n thanks, \n William")
