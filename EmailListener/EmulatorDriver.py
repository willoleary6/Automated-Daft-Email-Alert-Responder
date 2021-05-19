import os
import sys
import time
import subprocess
import config

sys.path.append('../')


def _is_connected_to_emulator(arr_response):
    for line in arr_response:
        if line.startswith(config.emulator_connection_name):
            return True
    return False


def _write_message(message):
    # open the text box
    time.sleep(config.short_wait_time_in_seconds)
    os.popen('adb -s ' + config.emulator_connection_name + ' shell input touchscreen tap 100 900').read()
    time.sleep(config.short_wait_time_in_seconds)
    os.popen('adb -s ' + config.emulator_connection_name + ' shell input text "' + config.Name.strip().replace(" ", "\ ")+ '"').read()

    # leaving option open as scam listings may be present
    if config.use_phone_number:
        time.sleep(config.short_wait_time_in_seconds)
        os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen tap 140 1200').read()
        time.sleep(config.short_wait_time_in_seconds)
        os.popen('adb -s '+config.emulator_connection_name+' shell input text "' + config.phone_number + '"').read()

    time.sleep(config.short_wait_time_in_seconds)
    os.popen('adb -s ' + config.emulator_connection_name + ' shell input touchscreen tap 140 1400').read()
    # we need to format the message as to allow proper spacing and for adb to write it
    lines = message.split("\n")
    for l in lines:
        time.sleep(config.short_wait_time_in_seconds)
        os.popen('adb -s '+config.emulator_connection_name+' shell input text "' + l.strip().replace(" ", "\ ") + '"').read()
        # next line
        time.sleep(config.short_wait_time_in_seconds)
        os.popen('adb -s '+config.emulator_connection_name+' shell input keyevent "KEYCODE_ENTER"').read()


def _navigate_to_add_listing():
    # opening gmail
    os.popen('adb -s '+config.emulator_connection_name+' shell monkey -p com.google.android.gm -v 1').read()
    time.sleep(config.long_wait_time_in_seconds)
    os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen tap 200 100').read()  # open folders
    time.sleep(config.short_wait_time_in_seconds)
    # swipe the options to bring the inFocus
    os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen swipe 200 1000 200 400 ').read()
    time.sleep(config.short_wait_time_in_seconds)
    # tap inFocus label
    os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen tap 200 600 ').read()
    time.sleep(config.short_wait_time_in_seconds)
    # close the folder button
    os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen tap 500 100 ').read()
    time.sleep(config.short_wait_time_in_seconds)
    # open daft ad
    os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen tap 1000 1000 ').read()
    # open the messaging screen
    time.sleep(config.x_long_wait_time_in_seconds)
    os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen tap 900 1850').read()


def _close_down_apps():
    time.sleep(config.short_wait_time_in_seconds)
    os.popen('adb -s '+config.emulator_connection_name+' shell am force-stop com.google.android.gm').read()
    time.sleep(config.long_wait_time_in_seconds)
    os.popen('adb -s '+config.emulator_connection_name+' shell am force-stop com.daft.ie').read()
    # ensuring the first app closed stays closed
    time.sleep(config.short_wait_time_in_seconds)
    os.popen('adb -s '+config.emulator_connection_name+' shell am force-stop com.google.android.gm').read()


def _spool_up_emulator(failed_attempts=0):
    if failed_attempts < 3:
        os.popen('adb connect '+config.emulator_connection_name).read()
        connected_devices = os.popen('adb devices -l').read().split('\n')
        connected_to_emulator = _is_connected_to_emulator(connected_devices)
        if not connected_to_emulator:
            # emulator is not running, create a new instance
            subprocess.Popen([config.emulator_executable_location])
            time.sleep(config.emulator_spool_up_time)  # wait a few minutes for blue stacks to spool up
            _spool_up_emulator(failed_attempts + 1)
    else:
        print("cant connect to emulator")
        sys.exit()


def message_landlord_on_emulator(message, logger):
    logger.info('-Setting up emulator -')
    os.chdir('C:\\adb\\platform-tools')  # This will change the present working directory
    # disconnect all devices first
    os.popen('adb disconnect').read()
    # reconnect to the emulator
    _spool_up_emulator()
    logger.info('-Navigating to ad listing -')
    _navigate_to_add_listing()

    logger.info('-Writing message -')
    # write message
    _write_message(message)

    # terms and conditions
    # Adding a configurable to check the terms and conditions box so we can test without actually emailing people
    if config.check_t_and_c_box:
        logger.info('-Checking T&C box -')
        time.sleep(config.short_wait_time_in_seconds)
        os.popen('adb -s localhost:5555 shell input touchscreen tap 55 1600').read()

    logger.info('- hitting send button -')
    # hit send message button
    time.sleep(config.short_wait_time_in_seconds)
    os.popen('adb -s '+config.emulator_connection_name+' shell input touchscreen tap 550 1800').read()
    logger.info('- Closing apps -')
    _close_down_apps()
