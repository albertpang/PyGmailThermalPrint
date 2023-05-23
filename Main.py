import time
import os
import imaplib
import email as em
from email.header import decode_header
import re

# from PIL import Image, ImageFilter

# IMAP stands for Internet Message Access Protocol
# I think it's the basis of the Apple Email App

class GmailIMAP():
    def __init__(self) -> None:
        '''Control the process of login, pulling, parsing from Gmail'''
        self.set_gmail_connection()

        counter = 1
        while True:
            print(f"\nStart Run Count: {counter}")
            self.read_email_inbox()
            print(f"End Run Count: {counter}")
            counter += 1
            time.sleep(20)


    def get_login(self) -> tuple:
        '''Read text file containing user and p/w for email account and returns
        tuple (user, password)
        Purposely not uploaded using git.ignore'''
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
        print("="*40)

    def move_folder(self, email_id):
        '''Moves the email to the printed folder'''
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


gm = GmailIMAP()

class ImageProcessing():
    def __init__(self) -> None:
        self.read_body()
        self.read_attachment()
        

# def triggerEmail():
# Default Setup of Email
def convertGrey(imageLocation):
    originalImage = "eakins.jpg"
    img = Image.open(originalImage)
    blurImage = img.filter(ImageFilter.BLUR)
    greyImage = blurImage.convert("1")
    greyImage.show()


# def clean(fileName) -> str:
#     return "FOLDER"

# def download_attachment(emailPart):
#     fileName = emailPart.get_filename()
#     if fileName:
#         folderName = clean(fileName)
#         if not os.path.isdir(fileName):
#             filePath = os.path.join(folderName,fileName)
#             open(filePath, "wb").write(emailPart.get_payload(decode=True))