import smtplib
from email.mime.text import MIMEText
import config

def send_email(sbj, msg):
    gmail_user = config.GUSER 
    gmail_password = config.GPASS
    text = msg
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = sbj
    msg['From'] = gmail_user
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(gmail_user, gmail_password)
    [server.sendmail(msg['From'], email, msg.as_string()) for email in config.EMAILS]
    server.quit()