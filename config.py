import re

email = 'jasmine.hales.hanks@gmail.com'
email_password = '9&@ym*vS4r4B1WCM*lP$amlD9F0n9IGt1'
csv_file_name = 'ArchivedEmails.csv'
default_csv_structure = 'sender,receiver,subject,date,status,file path'
default_sleep_time = 60 * 2  # 5 minutes
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
short_wait_time_in_seconds = 4
long_wait_time_in_seconds = 12
x_long_wait_time_in_seconds = 20
emulator_spool_up_time = 150
use_phone_number = False
phone_number = '0834740410'
Name = 'Jasmine Hales'
check_t_and_c_box = False


# Message

message = "Hi,\n \n" \
          "My name is William O Leary and my friends names are Alex White, Conor O Sullivan and Kiera Bracher. " \
          "We are interested in arranging a viewing of your rental property advertised on daft. " \
          "Your property is ideal for us as we want to move to somewhere quiet with a short commute " \
          "to our places of work. \n \n" \
          "I work as a software developer, Conor is a Data Scientist with AIB, " \
          "Alex is a mechanical engineer and Kiera is finishing her master's in law. " \
          "We have no pets and do not smoke.\n \n" \
          "We would be grateful if you could contact me by email to arrange a viewing. " \
          "We are ready to place a deposit and pay the first months rent upon viewing "\
          "the property and do not require any financial assistance to pay the rent. \n"\
          "We are available to move in to the property in June and " \
          "we can provide previous landlord references upon request. \n \n" \
          "I look forward to hearing from you soon,\n \n" \
          "Kind regards,\n" \
          "William O Leary"

# scraper
default_destination_super_folder = 'C:\\Users\\willo\\Google Drive\\Daft Automated responder'
chrome_driver = 'C:/Program Files/ChromeDriver/chromedriver.exe'
daft_image_url = 'https://photos.cdn.dsch.ie/'

