import datetime
import imaplib
import email
import sys
import config as config
import re
from DaftScraper import DaftScraper
from EmulatorDriver import message_landlord_on_emulator
from CsvHandler import CsvHandler
from email.header import decode_header

sys.path.append('../')


class Scanner:

    def __init__(self, logger):
        self._logger = logger
        self._email = config.email
        self._password = config.email_password
        self._smtp_server = config.smtp_server
        self._smtp_port = config.smtp_port
        self._mail_connection = self._initialise_connection_to_email()
        self._csv_handler = CsvHandler()

    def _initialise_connection_to_email(self):
        self._logger.info('- Connecting to email server ')
        mail = imaplib.IMAP4_SSL(self._smtp_server)
        mail.login(self._email, self._password)
        return mail

    def _parse_date(self, string_date):
        date_patterns = config.date_formats
        for pattern in date_patterns:
            try:
                return datetime.datetime.strptime(string_date, pattern)
            except:
                pass

        self._logger.Warning('- Date is not in expected format -')
        self._logger.Debug('- ' + string_date + ' ')
        self._logger.Warning('')
        sys.exit(0)

    def scan_email_inbox(self):
        status, messages = self._mail_connection.select('INBOX')
        self._logger.info(' Reading inbox-')
        self._logger.info(
            '-' + str(messages[0]) + ' emails in inbox-')
        list_of_emails = []

        for i in range(1, int(messages[0])+1):
            # need to parse her and rearrange
            useless_info, data = self._mail_connection.fetch(str(i), "(RFC822)")
            list_of_emails.append(data)
        email_indexes_in_order_of_date_time = self._rearrange_emails_by_datetime(list_of_emails)

        for j in range(len(email_indexes_in_order_of_date_time)):
            if email_indexes_in_order_of_date_time[j]['index'] > 0:
                self._parse_email(email_indexes_in_order_of_date_time[j]['index'])

    def _commit_email_to_persistent_storage(self, sender, receiver, subject, date, status, file_path=''):
        self._logger.info(' Saving email details in csv file ')
        # sender,receiver,subject,date,status,file path
        commit_dict = {
            'sender': sender,
            'receiver': receiver,
            'subject': subject,
            'date': date.strftime('%Y-%b-%d %H:%M:%S %z'),
            'status': status,
            'file path': file_path
        }
        self._csv_handler.write_to_csv_file(commit_dict)

    def _extract_url_from_email_body(self, data):
        # extract content type of email
        # get the email body
        self._logger.info(' Parsing body -')
        body = str(data.get_payload()[0])
        # format to parse links
        body = body.replace('=\n', '=')
        # get all the links
        matches = re.findall("(?P<url>https?://[^\s]+)", body)
        # return the first cus that's always the daft ad listing's link
        return matches[0]

    @staticmethod
    def _parse_uid(data):
        match = config.uid_pattern.match(data)
        return match.group('uid')

    def _copy_email_to_inFocus_folder(self, email_id):
        self._logger.info(
            '- Moving Email ' + str(email_id) + ' to label in gmail -')
        resp, data = self._mail_connection.fetch(str(email_id), "(UID)")
        msg_uid = self._parse_uid(data[0].decode('utf-8'))
        self._mail_connection.uid('COPY', msg_uid, config.InFocusGmailFolderName)

    def _rearrange_emails_by_datetime(self, list_of_emails):
        emails_indices_by_datetime = []
        for i in range(len(list_of_emails)):
            for response in list_of_emails[i]:
                if isinstance(response, tuple):
                    try:
                        # parse a bytes email into a message object
                        email_data = email.message_from_bytes(response[1])
                        received_date = self._parse_date(decode_header(email_data["Date"])[0][0])
                        emails_indices_by_datetime.append({'datetime': received_date, 'index': i})
                    except Exception as e:
                        print(e)
        return sorted(emails_indices_by_datetime, key=lambda x: x['datetime'])

    def _parse_email(self, email_index):
        typ, data = self._mail_connection.fetch(str(int(str(email_index))+1), "(RFC822)")
        for response in data:
            self._logger.info('- Reading CSV File ')
            self._csv_handler.read_csv_file()
            previously_scanned_emails = self._csv_handler.get_data_read_from_csv()

            if isinstance(response, tuple):
                try:
                    # parse a bytes email into a message object
                    email_data = email.message_from_bytes(response[1])
                    received_date = self._parse_date(decode_header(email_data["Date"])[0][0])
                    # decode the email subject
                    subject = decode_header(email_data["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode()
                    # email sender
                    sender = email_data.get("From")
                    receiver = self._email
                    status = 'Scanned'
                    if sender.find('Daft.ie Property Alert') > -1:
                        # need to see if the this email has already been cataloged
                        if (len(previously_scanned_emails)) > 0:

                            last_scanned_email = previously_scanned_emails[len(previously_scanned_emails)-1]
                            date_of_last_scanned_email = self._parse_date(last_scanned_email['date'])
                            if date_of_last_scanned_email < received_date:
                                self._process_email(sender, subject, received_date,
                                                    email_data, email_index, receiver, status)
                        else:
                            self._process_email(sender, subject, received_date,
                                                email_data, email_index, receiver, status)
                    else:
                        self._logger.info('- Not a property Alert email ')
                except Exception as e:
                    self._logger.warning(e)
                    self._logger.handlers[0].flush()
                    print(e)
                    sys.exit(0)

    def _process_email(self, sender, subject, received_date, email_data, email_index, receiver, status):
        self._logger.info('- New Email ! ')
        self._logger.info('Subject:' + str(subject))
        self._logger.info('From:' + str(sender))
        self._logger.info('Date:' + str(received_date))
        self._logger.info('')

        # scrape url
        scraper = DaftScraper(str(subject), self._extract_url_from_email_body(email_data))
        ##scraper.scrape_details()
        scraper.scrape_images()

        # copy the email into the InFocus folder so we can spool up and android emulator
        # open gmail -> navigate to the the InFocus folder and will select the first email in that
        # folder (Should be the one currently in memory)
        self._copy_email_to_inFocus_folder(email_index+1)
        # write message to landlord
        self._logger.info(' Launching emulator ')
        message_landlord_on_emulator(config.message, self._logger)

        self._commit_email_to_persistent_storage(sender, receiver, subject, received_date, status)
