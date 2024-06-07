from celery.app import shared_task
from django.conf import settings
from django.core.mail import send_mail

from django.template.loader import render_to_string


@shared_task
def send_invite_create_organisation(inviter, url, email):
    """
    This sends an email to a user to create an organisation on Rabah360.

    Params:
        inviter (str): The name of the person or organisation sending the invitation.
        url (str): The URL link for accepting the invitation and creating the organisation.
        email (str): The email address of the invitee.
    """
    html_message = f"""
    Dear User,<br/><br/>
    
    {inviter} has invited you to join Rabah360, a powerful church management platform. 
    To accept the invitation and create your account, please follow this <a href="{url}">link</a>.<br/><br/>
    
    Thank you,<br/>
    Rabah360 Team
    """
    html_message = render_to_string("email_template.html", {"message": html_message})
    send_mail(
        subject="Invitation to Create Organisation on Rabah360",
        message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )
    return True
