import os
import sys
import config 
import time
import logging
import datetime

from Scanner import Scanner

sys.path.append('../')


def _initialise_logger():
    x = datetime.datetime.now()
    log_file_directory = config.default_destination_super_folder+'\Logs'
    log_file_path = log_file_directory + '\EmailListener - ' + str(x.date()) + '.log'
    # if log file doesnt exist, create new
    if not os.path.exists(log_file_directory):
        os.makedirs(log_file_directory)

    try:
        open(log_file_path, 'r')
    except FileNotFoundError:
        open(log_file_path, 'w+')
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
    # blocking these libraries logging cus they just spam the file
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    return logging.getLogger()


def main():
    # initialise logger
    logger = _initialise_logger()
    logger.info('------------------------------------------------------------------------------------------------')
    logger.info('----------------------------------Beginning scan process----------------------------------------')
    logger.info('-----------------------------' + str(datetime.datetime.now()) + '-----------------------------------')

    count = 1
    # infinite loop, to check the emails
    while True:
        logger.info('-----------------------------Starting scan, checking emails---------------------------------')
        email_scanner = Scanner(logger)
        email_scanner.scan_email_inbox()

        count += 1
        logger.info('-----------------------------Scan Complete Going to sleep-----------------------------------')
        logger.info(
            '-----------------------------' + str(datetime.datetime.now()) + '-----------------------------------')
        logger.handlers[0].flush()
        logger = _initialise_logger()
        time.sleep(config.default_sleep_time)



if __name__ == '__main__':
    main()
