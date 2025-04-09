from django.db import models

from utils.currency import CurrencyAmount, precision, places


class Payment(models.Model):
    sender = models.ForeignKey("accounts.Account" , on_delete=models.SET_NULL, null=True, related_name="payment_sender")
    receiver = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null=True, related_name="payment_receiver")

    date = models.DateTimeField(auto_now_add=True)

    rate = models.DecimalField(max_digits=precision, decimal_places=places, null=False)

    sender_amount = models.DecimalField(max_digits=precision, decimal_places=places, null=False)
    receiver_amount = models.DecimalField(max_digits=precision, decimal_places=places, null=False)


    class Meta:
        indexes = [
            models.Index(fields=['sender', 'receiver', 'date'])
        ]
        ordering = ['-date']



class Request(models.Model):
    STATUS = [ 
        ("P", "Pending"),
        ("A", "Approved"), 
        ("D", "Denied")
    ]

    status = models.CharField(max_length=1, choices=STATUS,  null=False, default="P")

    
    sender = models.ForeignKey("accounts.Account" , on_delete=models.SET_NULL, null=True, related_name="request_sender")
    receiver = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null=True, related_name="request_receiver")
    
    date = models.DateTimeField(auto_now_add=True)
    
    rate = models.DecimalField(max_digits=precision, decimal_places=places, null=False)

    receiver_amount = models.DecimalField(max_digits=precision, decimal_places=places, null=False)
    sender_amount = models.DecimalField(max_digits=precision, decimal_places=places, null=False)


