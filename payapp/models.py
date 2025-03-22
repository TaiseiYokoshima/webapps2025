from django.db import models



class Payment(models.Model):
    sender = models.ForeignKey("accounts.Account" , on_delete=models.SET_NULL, related_name="sent_transactions", null=True)
    receiver = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, related_name="received_transactions", null=True)
    date = models.DateTimeField(auto_now_add=True)
    fee = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    rate = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)



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
        

    status = models.CharField(max_length=1, choices=STATUS, default="P", null=False)

    
    



