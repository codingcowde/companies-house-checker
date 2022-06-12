from email import encoders
from email.mime.base import MIMEBase
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_email(subject:str="CHecker", template:str="emails/notification", to:str="test@codingcow.de", data:dict = None, file:bytes=None):            
    if data is None:
        data = {}

    rich_text = render_to_string(template, data)
    plain_text = strip_tags(rich_text)
    
    mail = EmailMultiAlternatives(subject, plain_text, settings.EMAIL_HOST_USER, [to])
    mail.attach_alternative(rich_text, "text/html")
    if file:
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(file) ### feed out byte var
        encoders.encode_base64(payload) #encode the attachment
        #add payload header with filename
        payload.add_header('Content-Disposition', 'attachment; filename=your_data.txt')
        mail.attach(payload)
    mail.send()
    