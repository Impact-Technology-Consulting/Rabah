import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# Email configuration
EMAIL_PORT = 465
EMAIL_HOST = 'email-smtp.eu-north-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIA3QD2DQONNTLFTBXP'
EMAIL_HOST_PASSWORD = 'BNGeFVgbxysvpGOKIalOiFpmH2ZnIGI9JfTBIfTduUwo'
DEFAULT_FROM_EMAIL = 'support@rabah360.com'


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
