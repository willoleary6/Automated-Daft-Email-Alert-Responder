import datetime
import smtplib
import time
import imaplib
import email
import webbrowser
import os
import sys
import config
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

    def scan_email_inbox(self):
        self.mail_connection.select('inbox')
        email_type, data = self.mail_connection.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        print(id_list)
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(first_email_id, latest_email_id):
            typ, data = self.mail_connection.fetch(str(i), "(RFC822)")
            print(data)
            self.parse_email(data)

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

    def parse_email(self, data):
        for response in data:
            self.csv_handler.read_csv_file()
            previously_scanned_emails = self.csv_handler.get_data_read_from_csv()

            if isinstance(response, tuple):
                try:
                    # parse a bytes email into a message object
                    email_data = email.message_from_bytes(response[1])
                    print(decode_header(email_data["Date"])[0][0])
                    received_date = datetime.datetime.strptime(
                        decode_header(email_data["Date"])[0][0], '%a, %d %b %Y %H:%M:%S %z (%Z)')
                    # decode the email subject
                    subject = decode_header(email_data["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode()
                    # email sender
                    sender = email_data.get("From")
                    receiver = self._email
                    status = 'Scanned'
                    # print("Subject:", subject)
                    # print("From:", sender)
                    # print("Date:", received_date)
                    # need to see if the this email has already been cataloged
                    if (len(previously_scanned_emails)) > 0:
                        last_scanned_email = previously_scanned_emails[len(previously_scanned_emails) - 1]
                        date_of_last_scanned_email = datetime.datetime.strptime(
                            last_scanned_email['date'], '%Y-%b-%d %H:%M:%S %z')
                        if date_of_last_scanned_email < received_date:
                            print('test')
                            print(str(sender) + ' ' + str(receiver) + ' ' + str(subject) + ' ' + str(
                                received_date) + ' ' + str(status))
                            # self._commit_email_to_persistent_storage(sender, receiver, subject, received_date, status)

                    else:
                        print('Empty file')
                        print(str(sender) + ' ' + str(receiver) + ' ' + str(subject) + ' ' + str(
                            received_date) + ' ' + str(status))
                        self._commit_email_to_persistent_storage(sender, receiver, subject, received_date, status)
                except Exception as e:
                    print(e)
