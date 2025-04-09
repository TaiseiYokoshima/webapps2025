from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from  accounts.models import Account

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    fullname = forms.CharField(max_length=255, label="Full Name")

    class Meta:
        model = Account
        fields = ['email', 'username', 'password1', 'password2', "currency", ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        if not self.data.get('currency'):
            # sets the default 
            self.fields['currency'].initial = "GBP"

        self.fields['currency'].widget = forms.Select(choices=Account.CURRENCIES, attrs={'class':'currency-dropdown'})


    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        name_parts = fullname.split(" ", 1)

        if len(name_parts) != 2:
            raise forms.ValidationError("Fullname must provide both first and last name")

        first, last = name_parts



        if len(first) < 1:
            raise forms.ValidationError("Fullname must provide first name")

        if len(last) < 1:
            raise forms.ValidationError("Fullname must provide last name")


        self.first = first
        self.last = last

        return fullname


    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.first
        user.last_name = self.last

        user.save()
        return user

