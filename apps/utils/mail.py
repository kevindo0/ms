import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dynaconf import settings


def send_mail(subject, html, mail_to, to_name):
    mail_sender = 'games_note@wifi.com'

    msg = MIMEMultipart()
    msg.attach(MIMEText(html, 'html'))

    msg['Subject'] = subject
    msg['From'] = mail_sender
    msg['To'] = to_name

    with smtplib.SMTP("webmail.zenmen.com", 25) as smtp:
        smtp.login(mail_sender, settings.get('mail_pass'))
        smtp.sendmail(mail_sender, mail_to, msg.as_string())
