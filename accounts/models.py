from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Account(AbstractUser):
    CURRENCIES = [ 
        ("GBP", "GBP"),
        ("USD", "USD"), 
        ("EUR", "EUR")
    ]

    email = models.EmailField(unique=True, primary_key=True, null=False, blank=False)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=False, blank=False)
    username = models.CharField(max_length=1, blank=True, null=True, unique=True)
    

