import sys
import config
import time
from EmailListener.Scanner import Scanner
sys.path.append('../')


def main():
    print('-----------------------------------------------------------------------------------------------------------')
    print('--------------------------------------Beginning scan process-----------------------------------------------')
    print('-----------------------------------------------------------------------------------------------------------')

    count = 1
    # infinite loop, to check the emails
    while True:
        print('----------------------------------Starting scan, checking emails---------------------------------------')
        email_scanner = Scanner()
        email_scanner.scan_email_inbox()

        count += 1
        print('----------------------------------Scan Complete Going to sleep-----------------------------------------')
        time.sleep(config.default_sleep_time)


if __name__ == '__main__':
    main()
