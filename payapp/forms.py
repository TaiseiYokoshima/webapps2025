from django import forms

from accounts.models import Account

from utils.currency import CurrencyAmount

from typing import Tuple


class TransferForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}), max_length=254)
    amount = forms.DecimalField(label="Amount")

    def __init__(self, *args, user: Account|None=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is None:
            raise forms.ValidationError("Must provide the user")

        self.user: Account = user 

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email == self.user.email:
            raise forms.ValidationError("You cannot use your own email")

        try:
            self.checked_user = Account.objects.get(email=email)
        except Account.DoesNotExist: 
            raise forms.ValidationError("Account doesn't exist")

        return email


    def clean_amount(self):
        amount = self.cleaned_data.get("amount") 

        if amount is None:
            raise forms.ValidationError("Amount not provided")

        if amount < 1:
            raise forms.ValidationError("Minimum amount is 1.00 " + self.user.currency)

        amount_str = str(amount).split(".")

        if len(amount_str) == 2 and len(amount_str[1]) > 2:
            raise forms.ValidationError("Amount should be in the format 100.00. Only two decimal places are allowed.")


        self.amount: CurrencyAmount = CurrencyAmount(amount)
        return amount


    def get_payment_data(self) -> Tuple[Account, Account, CurrencyAmount]:
        sender: Account = self.user
        receiver = self.checked_user
        amount = self.amount

        return sender, receiver, amount


    def get_request_data(self) -> Tuple[Account, Account, CurrencyAmount]:
        receiver = self.user
        sender = self.checked_user
        amount = self.amount

        return sender, receiver, amount


