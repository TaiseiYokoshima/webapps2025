from django.db import models
from django.contrib.auth.models import AbstractUser


from decimal import Decimal


from utils.currency import precision, places


class Account(AbstractUser):
    CURRENCIES = [ 
        ("GBP", "GBP"),
        ("USD", "USD"), 
        ("EUR", "EUR")
    ]

    email = models.EmailField(unique=True, primary_key=True, null=False, blank=False)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=False, blank=False, default="GBP")
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    balance = models.DecimalField(max_digits=precision, decimal_places=places, default=Decimal("750.00"), null=False, blank=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @classmethod
    def get_default(cls, field_name: str):
        meta = getattr(cls, "_meta")
        return meta.get_field(field_name).default
    

