import re

email = 'william.o.leary.789@gmail.com'
email_password = 'NewHouseWithTheBois66!'
csv_file_name = 'ArchivedEmails.csv'
default_csv_structure = 'sender,receiver,subject,date,status,file path'
default_sleep_time = 60 * 5  # 5 minutes
smtp_server = 'imap.gmail.com'
smtp_port = 993
date_formats = [
    '%a, %d %b %Y %H:%M:%S %z (%Z)',
    '%a, %d %b %Y %H:%M:%S %z',
    '%Y-%b-%d %H:%M:%S %z',
    '%Y-%b-%d %H:%M:%S '
]
uid_pattern = re.compile('\d+ \(UID (?P<uid>\d+)\)')
InFocusGmailFolderName = 'InFocus'

# emulator driver
emulator_executable_location = 'C:\ProgramData\BlueStacks\Client\Bluestacks.exe'
emulator_connection_name = 'localhost:5555'
short_wait_time_in_seconds = 3
long_wait_time_in_seconds = 10
x_long_wait_time_in_seconds = 20
emulator_spool_up_time = 210
use_phone_number = True
phone_number = '0834740410'
