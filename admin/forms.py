from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from  accounts.models import Account

class AdminCreationForm(UserCreationForm):
    email = forms.CharField(max_length=255)

    class Meta:
        model = Account
        fields = [ 'password1', 'password2']

    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("This username is already in use")


        return email

    def save(self, commit=True):
        user = Account(
            email=self.cleaned_data['email'],
            is_superuser=True,
            is_staff=True,
        )
        user.set_password(self.cleaned_data["password1"])

        user.save()

        return user




