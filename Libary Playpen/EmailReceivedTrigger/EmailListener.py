import datetime
import smtplib
import time
import imaplib
import email
import webbrowser
import os
from email.header import decode_header

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "william.o.leary.789" + ORG_EMAIL
FROM_PWD = "NewHouseWithTheBois66!"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[2])
    print(id_list)
    for i in range(latest_email_id, first_email_id, -1):
        print(i)
        typ, data = mail.fetch(str(i), "(RFC822)")

        for response in data:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                received_date = datetime.datetime.strptime(decode_header(msg["Date"])[0][0], '%a, %d %b %Y %H:%M:%S %z')
                # decode the email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode()
                # email sender
                from_ = msg.get("From")
                print("Subject:", subject)
                print("From:", from_)
                print("Date:", received_date)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            #if filename:
                                #if not os.path.isdir(subject):
                                    # make a folder for this email (named after the subject)
                                    #os.mkdir(subject)
                                #filepath = os.path.join(subject, filename)
                                # download attachment and save it
                                #open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    if not os.path.isdir(subject):
                        # make a folder for this email (named after the subject)
                        os.mkdir(subject)
                    #filename = f"{subject[:50]}.html"
                    #filepath = os.path.join(subject, filename)
                    # write the file
                    #open(filepath, "w").write(body)
                    # open in the default browser
                    #webbrowser.open(filepath)
                print("=" * 100)


read_email_from_gmail()
