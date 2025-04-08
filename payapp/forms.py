from django import forms

from accounts.models import Account


from decimal import Decimal


from utils.currency import CurrencyAmount



from .models import Payment

class PaymentForm(forms.ModelForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}), max_length=254)
    amount = forms.DecimalField(label="Amount", min_value=1, max_digits=10, decimal_places=2)


    class Meta:
        model = Payment
        fields = ['receiver', 'amount']


    def __init__(self, *args, sender=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = sender 

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            self.receiver = Account.objects.get(email=email)
        except Account.DoesNotExist: 
            raise forms.ValidationError("User doesn't exist")

        return email


    def clean(self):
        if self.sender is None:
            raise forms.ValidationError("Sender not provided")

        amount_str: str | None = str(self.cleaned_data.get("amount"))

        if amount_str is None: 
            self.add_error("amount", "Amount not provided")
            return


        amount = CurrencyAmount(amount_str).into()
        
        balance = Decimal(self.sender.balance)

        if amount > balance:
            self.add_error("amount", "Insufficient Funds")
            return 


        def save(self, commit=True):
            payment = super().save(commit=False)
            payment.sender = self.user
            payment.recipient = self.recipient
            if commit:
                payment.save()
                # update balances
                self.user.balance -= payment.amount
                self.recipient.balance += payment.amount
                self.user.save()
                self.recipient.save()
            return 




    
