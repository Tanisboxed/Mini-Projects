import imaplib
import email 
import time
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

imap_server="imap.gmail.com"
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
target_org= "example.com"  #you have to replace this with the domain of target organisation
notification_email = os.getenv("NOTIFICATION_EMAIL")
smtp_server = "smtp.gmail.com"
smtp_port=587

def check_emails():
  mail= imaplib.IMAP4_SSL(imap_server)
  mail.login(email_address, email_password)
  mail.select("inbox")

  _, message_num= mail.search(None, f'(Unseen from "*@{target_org}")')
  for num in message_num[0].split():
    _, msg_data = mail.fetch(num, "(RFC822)")
    email_body = msg_data[0][1]
    email_message = email_message_from_bytes(email_body)
    subject= email_message["subject"]
    sender = email_message["from"]
    send_notification(subject, sender)
    mail.store(num, "+FLAGS","\\Seen")
  mail.logout()

def send_notif(subject,sender):
  msg= MIMEText(f"New email from {sender}\nSubject: {subject}")
  msg['Subject']=f"New email from {target_org}"
  msg['From']=email_address
  msg['to'] = notifcation_email
  with smtplib.SMTP(smtp_server,smtp_port) as server:
    server.starttls()
    server.login(email_address, email_password)
    server.send_message(msg)

def main():
  while True: 
    check_emails()
    time.sleep(1800)

if __name__ == "__main__":
  main()
  



