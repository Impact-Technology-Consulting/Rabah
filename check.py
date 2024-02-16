import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rabah.settings')
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from django.conf import settings

# Email configuration
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_HOST_USER = settings.EMAIL_HOST
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST
DEFAULT_FROM_EMAIL = settings.EMAIL_HOST


def send_email(subject, message, recipient_email):
    try:
        # Create a MIMEText object
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Rabah Support', DEFAULT_FROM_EMAIL))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, 'plain'))

        # Establish a connection to the SMTP server
        server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        server.ehlo()

        # Login to the SMTP server
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        # Send the email
        server.sendmail(DEFAULT_FROM_EMAIL, recipient_email, msg.as_string())

        # Close the connection
        server.close()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Example usage
subject = "Test Email"
message = "This is a test email sent using Python's smtplib and AWS SES."
recipient_email = "dev.codertjay@gmail.com"
send_email(subject, message, recipient_email)
