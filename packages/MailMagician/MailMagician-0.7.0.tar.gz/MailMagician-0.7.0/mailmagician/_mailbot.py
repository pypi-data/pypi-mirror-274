import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
import os

class Attachment:
    def __init__(self,filename:str, payload:bytes) -> None:
        self.filename = filename
        self.payload = payload

class Mailbot():
    def __init__(self, email_account: str, password: str, smtp_server: str = 'smtp.126.com'):
        self.gmail_user = email_account
        self.gmail_password = password
        self.smtp_server = smtp_server

    def send(self, sentTo, subject, msgBody, attachment:Attachment=None):
        gmail_user = self.gmail_user
        sent_from = self.gmail_user
        gmail_password = self.gmail_password
        email_text = msgBody

        msg = MIMEMultipart()
        msg["Subject"] = Header(subject, charset='utf-8')
        msg["From"] = gmail_user
        msg["To"] = sentTo

        msg.attach(MIMEText(email_text, 'plain', 'utf-8'))

        if attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.payload)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment.filename}"')
            msg.attach(part)

        try:
            server = smtplib.SMTP_SSL(self.smtp_server)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, sentTo, msg.as_string())
            server.close()

            print('Email sent!')
        except Exception as e:
            print('Something went wrong...')
            raise e