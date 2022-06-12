from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_email(subject:str="CHecker", template:str="emails/notification", to:str="test@codingcow.de", data:dict = None):            
    if data is None:
        data = {}

    rich_text = render_to_string(template, data)
    plain_text = strip_tags(rich_text)
    
    mail = EmailMultiAlternatives(subject, plain_text, settings.EMAIL_HOST_USER, [to])
    mail.attach_alternative(rich_text, "text/html")
    mail.send()
    