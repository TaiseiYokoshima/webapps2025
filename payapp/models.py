from django.db import models

from utils.currency import CurrencyAmount, precision, places


from django.dispatch import receiver
from django.db.models.signals import post_save


class Payment(models.Model):
    sender = models.ForeignKey("accounts.Account" , on_delete=models.SET_NULL, null=True, related_name="payment_sender")
    receiver = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null=True, related_name="payment_receiver")

    date = models.DateTimeField(auto_now_add=True)

    rate = models.DecimalField(max_digits=precision, decimal_places=places, null=False)

    sender_amount = models.DecimalField(max_digits=precision, decimal_places=places, null=False)
    receiver_amount = models.DecimalField(max_digits=precision, decimal_places=places, null=False)

    from_request = models.BooleanField(null=False, default=False)


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



class Notification(models.Model):
    STATUS = [
        ("U", "Unread"),
        ("R", "Read"),
    ]

    n_type = [
        ("P", "Payment"),
        ("R", "Request"),

    ]

    date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=1, choices=STATUS,  null=False, default="U")
    n_type = models.CharField(max_length=1, choices=STATUS, null=False)
    payment = models.ForeignKey("payapp.Payment" , on_delete=models.SET_NULL, null=True, related_name="payment_id")
    request = models.ForeignKey("payapp.Request" , on_delete=models.SET_NULL, null=True, related_name="request_id")
    user = models.ForeignKey("accounts.Account" , on_delete=models.CASCADE, related_name="notification_owner")
    message = models.CharField(max_length=200, null=False)


    class Meta:
        indexes = [
            models.Index(fields=[ 'date'])
        ]
        ordering = ['-date']


    
@receiver(post_save, sender=Request)
def notify_request(sender, instance, created, *args, **kwargs):
    request = instance

    user = request.receiver
    subject = request.sender

    amount = CurrencyAmount(request.receiver_amount).to_api_str()

    if created:
        message = f"{subject.email} requested {amount} {user.currency}."
        notification = Notification(
            n_type="R",
            request=request, 
            user=user,
            message=message
        )

        try:
            notification.save()
        except Exception as e:
            print(e)

        return


    request_status = request.status

    status_str = "approved"


    if request_status == "D":
        status_str = "denied"

    elif request_status == "A":
        pass
    else:
        raise Exception("Request notification trigged when not approved or denied")
        

    message = f"{subject.email} has {status_str} your request of {amount} {user.currency}."


    notification = Notification(
        n_type="R",
        request=request, 
        user=user,
        message=message
    )

    try:
        notification.save()
    except Exception as e:
        print(e)


    return


@receiver(post_save, sender=Payment)
def notify_payment(sender, instance, created, *args, **kwargs):
    print("payment notification called")
    payment = instance


    if not created:
        raise Exception("payment notification called when not created")

    if payment.from_request:
        return


    user = payment.receiver
    subject = payment.sender
    amount = CurrencyAmount(payment.receiver_amount).to_api_str()

    message = f"{subject.email} has transfered you {amount} {user.currency}."
    notification = Notification(
        n_type="P",
        payment=payment, 
        user=user,
        message=message
    )

    try:
        notification.save()
        print("payment notification saved")
    except Exception as e:
        print(e)

    return


