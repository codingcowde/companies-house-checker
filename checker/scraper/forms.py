from django.forms import ModelForm, ValidationError
from django.core.validators import validate_email
from .models import Subscription
import re

# Used to validate the Subscription Form Data
class SubscribeForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'email']
    
    def clean(self):
        super(SubscribeForm, self).clean()
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']        

        try:
            validate_email( email )                   
        except ValidationError:            
            self._errors['email'] = self.error_class(['Email not valid!']) 
        
        if len(name) < 5:            
            self._errors['name'] = self.error_class(['Please provide your fullname!'])              
        else:
            #clean name from special chars to avoid xss 
            name = re.sub("[^\w\s!?]","", name)
            self.cleaned_data['name'] = name        

        return self.cleaned_data

# Used to validate emails 
class EmailForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

    def clean(self):
        super(EmailForm, self).clean()        
        email = self.cleaned_data['email']
        try:
            validate_email( email )                    
        except ValidationError:
            self._errors['email'] = self.error_class(['Email not valid!'])        
        return self.cleaned_data

        
            

