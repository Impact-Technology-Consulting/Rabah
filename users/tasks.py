from celery import shared_task
from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

Rabah_INFO_MAIL = config("Rabah_INFO_MAIL")
Rabah_CUSTOMER_SUPPORT_MAIL = config("Rabah_CUSTOMER_SUPPORT_MAIL")


@shared_task
def send_member_activate_account(inviter, url, email, first_name, last_name):
    """
    This sends an email to the logged-in user for verification
    """
    html_message = f"""
    Dear {first_name} {last_name} <br/>
    
    {inviter} has invited you to join Rabah360, a powerful church management platform. To accept the invitation and create your account, please follow this: <a href="{url}">link</a>
 <br/>

Thank you  <br/>
Rabah360 Team
        """
    html_message = render_to_string("email_template.html", {"message": html_message})
    send_mail(
        recipient_list=[email],
        subject="Invitation to Join Rabah360",
        message=html_message,
        html_message=html_message,
        fail_silently=False,
    )
    return True


@shared_task
def send_welcome_email(email, first_name):
    """
    This sends a welcome email to new users
    """
    html_message = f"""
    Dear {first_name},<br/><br/>

    Welcome to Rabah360! We are thrilled to have you join our community and embark on this journey of streamlined church management together. Our mission is to empower your ministry and support you in every step of your church's growth.<br/><br/>

    As you start using Rabah360, we want to ensure you have a smooth and enjoyable experience. Here are a few key steps to get you started:<br/><br/>

    <b>Explore Our Features:</b> Dive into our comprehensive suite of features designed specifically for churches. From People Management to Attendance Tracking, Groups, Giving & Finances, Analytics, and more, Rabah360 has everything you need to manage your church effectively.<br/><br/>

    <b>Need Help? We're Here for You:</b> Our support team is dedicated to assisting you every step of the way. If you have any questions, encounter any issues, or simply need guidance, don't hesitate to reach out. You can contact us at <a href="mailto:support@rabah360.com">support@rabah360.com</a>.<br/><br/>

    <b>Stay Updated:</b> Keep an eye on your inbox for important updates, tips, and best practices to make the most out of Rabah360. We'll also share exciting news about upcoming features and enhancements.<br/><br/>

    Once again, thank you for choosing Rabah360 as your church management solution. We're committed to helping you achieve your ministry goals and look forward to partnering with you on this journey.<br/><br/>

    Warm regards,<br/>
    Pastor Bahram Ghebray<br/>
    CEO<br/>
    Rabah360
    """
    send_mail(
        recipient_list=[email],
        subject="Welcome to Rabah360: Your Church Management Solution",
        message=strip_tags(html_message),
        html_message=html_message,
        fail_silently=False,
    )
    return True


