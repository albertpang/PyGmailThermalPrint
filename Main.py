import time
import imaplib
import email as em
from email.header import decode_header
import re

# IMAP stands for Internet Message Access Protocol
class GmailIMAP():
    def __init__(self) -> None:
        '''Control the process of login, pulling, parsing from Gmail'''
        self.set_gmail_connection()
        self.read_email_inbox()

    def get_login(self) -> tuple:
        '''Read text file containing user and p/w for email account and returns
        tuple (user, password) '''

        # Purposely not uploaded using git.ignore
        loginFile = open("login.txt", "r")
        username = loginFile.readline().strip()
        password = loginFile.readline()
        return(username, password)
    
    def set_gmail_connection(self):
        '''Set up IMAP with gmail account'''
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        user, pw = self.get_login()
        self.imap.login(user, pw)      

    def read_email_inbox(self):
        '''Reads all emails found in the email inbox'''
        self.imap.select("Inbox", readonly=False)
        _, items = self.imap.search(None, 'All')
        email_ids  = items[0].split()

        # Retrieve the UIDs and message numbers of all emails in the inbox
        for email_id in email_ids:
            resp, emailInbox = self.imap.fetch(email_id, "(RFC822)")
            for msg in emailInbox:
                # If the email is a tuple
                if isinstance(msg, tuple):
                    # format email from bytes
                    email = em.message_from_bytes(msg[1])
                    self.pull_metadata(email)
            self.move_folder(email_id)

    def pull_metadata(self, email):
        '''Takes the Email object and pulls metadata using decode_header method'''
        title = decode_header(email["Subject"])[0]        
        receiveTime = decode_header(email["Date"])[0]
        sender = decode_header(email['From'])[0]
        
        print(f'Subject: {title[0]}')
        print(f'Received: {receiveTime[0]}')
        print(f'From: {sender[0]}')

        # Retrieve and print the email body
        if email.is_multipart():
            for part in email.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print(f"Body:{body}")
        else:
            body = email.get_payload(decode=True)
            decodedBody = body.decode()
            print(f"Body: {decodedBody}")
        print("="*70)

    def move_folder(self, email_id):
        '''Moves the email to the Printed label and removes the Inbox label'''
        # Get the UID of the email to be moved
        # Move the email to the printed folder
        pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')

        def parse_uid(data):
            if data is None:
                return None
            match = pattern_uid.match(data.decode('utf-8'))
            return match.group('uid')
        
        # Loop through the data and retrieve the corresponding emails
        uid_data = self.imap.fetch(email_id, "(UID)")[1]
        uid = parse_uid(uid_data[0])
        if uid:
            self.imap.uid('COPY', uid, 'Printed')
            self.imap.uid('STORE', uid , '+FLAGS', '(\Deleted)')
            self.imap.expunge()


if __name__ == "__main__":
    print("==================")
    print(" THERMAL PRINTER ")
    print("==================")
    
    while True:
        gm = GmailIMAP()
        time.sleep(120)