import datetime
import smtplib
import time
import imaplib
import email
import webbrowser
import os
import sys
import config
from EmailListener.EmulatorDriver import message_landlord_on_emulator
from EmailListener.CsvHandler import CsvHandler

sys.path.append('../')

from email.header import decode_header


class Scanner:

    def __init__(self):
        self._email = config.email
        self._password = config.email_password
        self._smtp_server = config.smtp_server
        self._smtp_port = config.smtp_port
        self.mail_connection = self._initialise_connection_to_email()
        self.csv_handler = CsvHandler()

    def _initialise_connection_to_email(self):
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

        print("Date is not in expected format: %s" % string_date)
        sys.exit(0)

    def scan_email_inbox(self):
        status, messages = self.mail_connection.select('INBOX')
        for i in range(int(messages[0]), 0, -1):
            self.parse_email(i)

    def _commit_email_to_persistent_storage(self, sender, receiver, subject, date, status, file_path=''):
        # sender,receiver,subject,date,status,file path
        commit_dict = {
            'sender': sender,
            'receiver': receiver,
            'subject': subject,
            'date': date.strftime('%Y-%b-%d %H:%M:%S %z'),
            'status': status,
            'file path': file_path
        }
        self.csv_handler.write_to_csv_file(commit_dict)

    def _parse_body(self, data):
        # extract content type of email
        content_type = data.get_content_type()
        # get the email body
        # will be an array first index is the plain text while the second is the html
        body = data.get_payload()[0]
        print('----------------------------')
        print(body)

    @staticmethod
    def _parse_uid(data):
        match = config.uid_pattern.match(data)
        return match.group('uid')

    def _copy_email_to_inFocus_folder(self, email_id):
        resp, data = self.mail_connection.fetch(str(email_id), "(UID)")
        msg_uid = self._parse_uid(data[0].decode('utf-8'))
        self.mail_connection.uid('COPY', msg_uid, config.InFocusGmailFolderName)

    def parse_email(self, email_index):
        typ, data = self.mail_connection.fetch(str(email_index), "(RFC822)")
        for response in data:
            self.csv_handler.read_csv_file()
            previously_scanned_emails = self.csv_handler.get_data_read_from_csv()

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
                    # need to see if the this email has already been cataloged
                    if (len(previously_scanned_emails)) > 0:
                        last_scanned_email = previously_scanned_emails[len(previously_scanned_emails) - 1]
                        date_of_last_scanned_email = self._parse_date(last_scanned_email['date'])
                        if date_of_last_scanned_email < received_date:
                            print("Subject:", subject)
                            print("From:", sender)
                            print("Date:", received_date)
                            self._parse_body(email_data)
                            # copy the email into the InFocus folder so we can spool up and android emulator
                            # open gmail -> navigate to the the InFocus folder and will select the first email in that
                            # folder (Should be the one currently in memory)
                            self._copy_email_to_inFocus_folder(email_index)

                            # write message to landlord
                            message_landlord_on_emulator(
                                "Hi, \n is this property still available? \n thanks, \n William")

                            self._commit_email_to_persistent_storage(sender, receiver, subject, received_date, status)

                    else:
                        print("Subject:", subject)
                        print("From:", sender)
                        print("Date:", received_date)
                        self._copy_email_to_inFocus_folder(email_index)
                        # write message to landlord
                        message_landlord_on_emulator("Hi, \n is this property still available? \n thanks, \n William")
                        self._commit_email_to_persistent_storage(sender, receiver, subject, received_date, status)
                except Exception as e:
                    print(e)
