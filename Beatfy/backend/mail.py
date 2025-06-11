from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib

SMTP_SERVER_HOST= "localhost"
SMTP_SERVER_PORT= 1025
SENDER_ADDRESS = "support@beatfy.com"
SENDER_PASSWORD = ""

def send_mail(receiver, subject, message, content="text"):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receiver
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP(host = SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)
    server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

    return 'Mail Sent successfully !!'