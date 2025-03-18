from django.db import models
from django.contrib.auth.models import AbstractUser

from decimal import Decimal


class Account(AbstractUser):
    CURRENCIES = { 
        "GBP": "GBP",
        "USD": "USD", 
        "EUR": "EUR"
    }

    email = models.EmailField(unique=True, primary_key=True, null=False, blank=False)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=False, blank=False, default="GBP")
    username = models.CharField(max_length=1, blank=True, null=True, unique=True)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=Decimal("750.00"), null=False, blank=False)


    def get_default(field_name: str):
        return Account._meta.get_field(field_name).default
    

