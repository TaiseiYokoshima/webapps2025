from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from  accounts.models import Account

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['email', 'password1', 'password2', "currency"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].initial = "GBP"
        self.fields['currency'].widget = forms.Select(choices=Account.CURRENCIES, attrs={'class':'currency-dropdown'})
