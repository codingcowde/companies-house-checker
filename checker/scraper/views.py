from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template import loader
from .models import Subscription, load_zero_flagged_from_database, load_flagged_from_database, set_flag
from .forms import EmailForm, SubscribeForm
from .scraper import CHeckerScraper as CHS
from django.core.mail import send_email
from django.conf.global_settings import EMAIL_HOST_USER
import time, random

# Create your views here.

def index(request):
    """ the sole interface of the app providing all 3 forms for more details,
        check the template
    """
    template = loader.get_template('index.html')
    
    context= {}
    
    return HttpResponse(template.render(context, request))

def subscribe(request) -> HttpResponseRedirect:
    """ create a new Subscription  
        triggers an email confirmation on success 
        and redirects the user to /#register    
    """
    form = SubscribeForm(request.POST or "")        
    if request.method != 'POST' or not form.is_valid():           
        return HttpResponseRedirect('/#error')            

    subscription  = form.save()
    subscription.save()  
    # Send the confirmation email
    email_template = loader.get_template('emails/subscribe.htm').render({})
    send_mail(
        'Welcome to CHecker',
        f'{email_template}',
        form.cleaned_data['email']
    )    
    return HttpResponseRedirect('#register')
 

def unsubscribe(request) -> HttpResponseRedirect:
    """ deletes all entrys matching the email address 
        triggers an email confirmation on success 
        and redirects the user to /#unsubscribe    
    """
    form = EmailForm(request.POST or "")
    if request.method != 'POST' or not form.is_valid():
        return HttpResponseRedirect('/#error')
    
    if subscriptions := Subscription.objects.filter(email = form.cleaned_data["email"]):
        for sub in subscriptions:
            sub.delete()   
        # Now we send the email confirming the deletion of all data
        # connected to the email.
        # We won't spam users with multiple entrys    
        email_template = loader.get_template('emails/unsubscribe.htm').render({})
        send_mail(
            'You are unsubscribed from CHecker - All data has been deleted',
            f'{email_template}',
             form.cleaned_data["email"])    
    return HttpResponseRedirect('/#unsubscribe')

def request_data_export(request) -> HttpResponseRedirect:
    """ checks for existing subscriptions and
        triggers an email with data on success 
        and redirects the user to /#download    
    """
    form = EmailForm(request.POST or "")
    if request.method != 'POST' or not form.is_valid():
            return HttpResponseRedirect('/#error')
    email = form.cleaned_data['email']
    
    # Get all data connected to the given email
    if subscribed := Subscription.objects.filter(email = email):
        # Now send email with all information found for the given email.
        # Again no spamming of users with multiple entrys
        email_template = loader.get_template('emails/export.htm').render({subscribed})        
        send_mail(
            'Your Data Export From CHecker',
            f'{email_template}',
            email
            )
    #send response
    return HttpResponseRedirect('/#download')

 
def run_scraper(request):
    """ should be called from chron tab or similar
        Runs the scraping job and triggers email notifications
        needs authentication

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    if not request.user.is_authenticated or request.method != 'POST':
        return HttpResponseRedirect('/#error')
    flagged = load_flagged_from_database()
    unflagged = load_zero_flagged_from_database()

    for user in flagged:
        user.flag -= 1
        user.save()

    for user in unflagged:
       if result := CHS.run(user.name):
            ### implement the logic needed to build report
            #  from legacy main.py in the template emails/notification.htm
            email_template = loader.get_template('emails/notification.htm').render({
                'result':result,
                'user':user,
                })                                    
            send_mail(
                'Your Report from CHecker',
                f'{email_template}',
                user.email
            )
            set_flag(user.name, user.email)
            # SLEEP AFTER EVERY REQUEST TO AVOID SPAMMING THE SERVER    
            seconds = random.randint(10, 60)                    
            time.sleep(seconds)

def send_mail(subject, template, to):
    send_email(subject,template, EMAIL_HOST_USER, [f'{to}'])