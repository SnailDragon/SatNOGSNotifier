import privateSettings
import smtplib
import ssl
from email.message import EmailMessage

##
# Takes an array of emails, a subject, and body and sends an email from the 
# email provided in privateSettings.py 
##
def notifyOwners(recipientEmails, subject, body):
    email_sender = privateSettings.MY_EMAIL
    email_password = privateSettings.GMAIL_LOGIN_KEY
    email_receiver = ", ".join(recipientEmails)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
