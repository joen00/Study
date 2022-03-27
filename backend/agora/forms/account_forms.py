from django import forms
from django.db.models.fields import EmailField
from django.db import transaction

from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage

from allauth.account.forms import LoginForm, SignupForm

import threading
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from agora.models import ONEUser
from agora.token import *


class testForm(forms.Form):
    a = forms.CharField(max_length=1)

class ONEUserSignupForm(SignupForm):
    username = forms.CharField(max_length=20)
    class Meta:
        model = ONEUser
        fields = ('username', 'email','password1', 'password2', )
    """
    @transaction.atomic
    def save(self, request):
        new_user =  super().save(request)
        new_user.is_active = False
        # email varification process
        uidb64 = urlsafe_base64_encode(force_bytes(new_user.id))
        token = account_activation_token.make_token(new_user) # from token.py
        message_data = message("localhost:8000", uidb64, token) # from token.py
        # email sending requires long-burst
        self.thread_maker(message_data, new_user.email)
        return new_user

    def email_sender(self, message, destination):   
        email = EmailMessage("email 인증",message,to=[destination])
        email.send()
    
    def thread_maker(self, message, destination):
        thread = threading.Thread(target=self.email_sender, args=(message, destination))
        thread.start()
    """

class ONEUserLoginForm(LoginForm):
    class Meta:
        model = ONEUser  
