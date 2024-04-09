from celery import shared_task
from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

Rabah_INFO_MAIL = config("Rabah_INFO_MAIL")
Rabah_CUSTOMER_SUPPORT_MAIL = config("Rabah_CUSTOMER_SUPPORT_MAIL")


@shared_task
def send_member_activate_account(url, email, first_name, last_name):
    """
    This sends an email to the logged-in user for verification
    """
    html_message = f"""
    Hello {first_name} {last_name}, <br/>
    
    Kindly click the <a href="{url}">link</a>   below to activate your account <br/>


Regards,<br/>
Rabah Team <br/> <br/>
This email has been sent to persons who have requested to create accounts 
on the Rabah platform.<br/><br/>  
If you didn't register, please click
<a href='#'>Unsubscribe</a>
        """
    html_message = render_to_string("email_template.html", {"message": html_message})
    send_mail(
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        subject="Member Account Activation",
        message=html_message,
        html_message=html_message,
        fail_silently=False,
    )
    return True
