import os
import imaplib
import email as em
from email.header import decode_header

# from PIL import Image, ImageFilter

# IMAP stands for Internet Message Access Protocol
# I think it's the basis of the Apple Email App

class GmailIMAP():
    def __init__(self) -> None:
        '''Control the process of login, pulling, parsing from Gmail'''
        self.set_gmail_connection()
        self.read_email_inbox()

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
        print(self.imap.list())
        messages = self.imap.select("[GMAIL]/INBOX")[1]
        numOfMessages = int(messages[0])
        for i in range(numOfMessages, 0, -1):
            # use RFC822 email message format to decode email
            emailInbox = self.imap.fetch(str(i), "(RFC822)")[1]
            for msg in emailInbox:
                # If the email is a tuple
                if isinstance(msg, tuple):
                    # format email from bytes
                    email = em.message_from_bytes(msg[1])
                    self.pull_metadata(email)
                    print("="*100)
    
    def pull_metadata(self, email):
        '''Takes the Email object and pulls metadata using decode_header method'''
        title = decode_header(email["Subject"])[0]        
        receiveTime = decode_header(email["Date"])[0]
        sender = decode_header(email['From'])[0]
        print(f'Subject: {title[0]}')
        print(f'Received: {receiveTime[0]}')
        print(f'From: {sender[0]}')


# class Email():
#     def __init__(self) -> None:
#         self._title = 
#         self._from = 
#         self._to = 

    
       

gm = GmailIMAP()


class ImageProcessing():
    def __init__(self) -> None:
        self.read_body()
        self.read_attachment()
        







def obtain_header(msg):
    # decode the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
 
    # decode email sender
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding)
 
    print("Subject:", subject)
    print("From:", From)
    return subject, From

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