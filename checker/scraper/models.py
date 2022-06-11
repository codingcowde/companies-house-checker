import uuid
from django.db import models

# Create your models here.

## Subscription model for subscribed users - contains uuid as index, name/search term and email address
class Subscription(models.Model):
    # create an UUID for the subscription
    id = models.UUIDField(
        primary_key = True,
         default = uuid.uuid4,
          editable = False
          )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    flag = models.IntegerField(0)

### test these functions to work with django db

def load_zero_flagged_from_database() -> list:
    """loads the names from the database which have flag 0"""  
    result = Subscription.objects.filter(flag = 0)
    return list(result)       
   

def load_flagged_from_database() -> list:
    """loads the names from the database which have flag not 0"""          
    result = Subscription.objects.filter(flag__gt = 0 )
    return list(result)  

def set_flag(name, email) -> None:
    """sets the flag to 10 meaning the user won't be notified for 10 cycles"""
    if result := Subscription.objects.filter(name = name, email = email )[:1][0]
        result.set(flag = 10)
        result.save()
    


