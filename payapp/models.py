from django.db import models


class Payment(models.Model):
    sender = models.ForeignKey("accounts.Account" , on_delete=models.SET_NULL, null=True, related_name="payment_sender")
    receiver = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null=True, related_name="payment_receiver")
    date = models.DateTimeField(auto_now_add=True)
    fee = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    rate = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, null=False)


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
    fee = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    rate = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    



