import email
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template import loader
from .models import Subscription, load_zero_flagged_from_database, load_flagged_from_database, set_flag
from .forms import EmailForm, SubscribeForm
from .scraper import CHeckerScraper 
from .mail import send_email


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
    form = SubscribeForm(request.POST or None)   

    if request.method != 'POST' :           
        return HttpResponseRedirect('/#error')            
    if form.is_valid():
        subscription  = form.save()
        subscription.save()  

        # Send the confirmation email        
        email=form.cleaned_data['email']        
        send_email(
            subject ='Welcome to CHecker',
            template = 'emails/subscribe.htm',
            to = email,                
            data = {
                'request':request.POST,
                }
        )
    return HttpResponseRedirect('/#register')
 

def unsubscribe(request) -> HttpResponseRedirect:
    """ deletes all entrys matching the email address 
        triggers an email confirmation on success 
        and redirects the user to /#unsubscribe    
    """
    form = EmailForm(request.POST or "")
    if request.method != 'POST' or not form.is_valid():
        return HttpResponseRedirect('/#error')
    
    if subscriptions := Subscription.objects.filter(email = form.cleaned_data["email"]):
        # get the data export before deleting the entries
        file = create_data_export(subscriptions)

        for sub in subscriptions:
            sub.delete()   
        # Now we send the email confirming the deletion of all data
        # connected to the email.
        # We won't spam users with multiple entrys    
        email = form.cleaned_data["email"]        
        send_email(
                'You are unsubscribed from CHecker - All data has been deleted',
                'emails/unsubscribe.htm',
                email,   
                {},
                file
            )
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

        file = create_data_export(subscribed)
        send_email(
            'Your Data Export From CHecker',
            'emails/export.htm',
            email,
            {},
            file
        )
    #send response
    return HttpResponseRedirect('/#download')

def create_data_export(subscribed) -> bytes:
    result = "uuid, name, email, flag \n"
    for sub in subscribed:
        result += f"{sub.id}, {sub.name}, {sub.email}, {sub.flag} \n"
    return bytes(result,'utf-8')

 
def run_scraper(request):
    """ should be called from chron tab or similar
        Runs the scraping job and triggers email notifications
        needs authentication
    """
   # if not request.user.is_authenticated or request.method != 'POST':
   #     return HttpResponseRedirect('/#error')
    flagged = load_flagged_from_database()
    unflagged = load_zero_flagged_from_database()

    for user in flagged:
        user.flag -= 1
        user.save()
    CHS = CHeckerScraper()
    for user in unflagged:
        print(f"we have unflagged user: {user.name}")
        if result := CHS.run(user.name):
            ### implement the logic needed to build report
            #  from legacy main.py in the template emails/notification.htm
            print("found one")
            send_email(
                'Your Report from CHecker',
                'emails/notification.htm',
                user.email,
                {
                'result':result,
                'user':user,
                }
            )
            set_flag(user.name, user.email)
            # SLEEP AFTER EVERY REQUEST TO AVOID SPAMMING THE SERVER    
            seconds = random.randint(10, 60)                    
            time.sleep(seconds)
    return HttpResponse("Ran scrape job")
