from decimal import Decimal
from enum import Enum

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from services.currency import CurrencyAmount, call_conversion_api
from django.db import transaction


from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect


from django.db.models import Q


from django.contrib import messages


from typing import Union, Type

from accounts.models import Account
from .models import Payment
from .models import Request



from .forms import TransferForm


class TransferResult(Enum):
    Ok = "success"
    InsufficientFunds = "Failed to make payment due to insufficient funds"
    CurrencyExchangFaillure = "Server error due to currency conversion"
    InvalidStringValueForAmount = "Invalid string value for currency amount"
    TransactionFailure = "Server error due to transaction failure"


@transaction.atomic()
def make_transfer(request, sender: Account, receiver: Account, amount_str: CurrencyAmount, Model: Union[Type[Payment], Type[Request]]) -> TransferResult:
    amount = None
    rate = CurrencyAmount(1)

    try:
        amount = CurrencyAmount(amount_str)
    except Exception:
        return TransferResult.InvalidStringValueForAmount

    source: str = getattr(sender, "currency")
    target: str = getattr(receiver, "currency")
    sender_balance = CurrencyAmount(getattr(sender, "balance"))
    receiver_balance = CurrencyAmount(getattr(receiver, "balance"))

    sender_subtract = amount
    receiver_add = amount

    if (Model is Payment and sender.balance < amount.into()):
        return TransferResult.InsufficientFunds


    if (source != target):
        try:
            result_json = call_conversion_api(request, source, target, str(amount_str.into()))
            receiver_add = CurrencyAmount(result_json["amount"])
            rate = CurrencyAmount(Decimal(result_json["amount"]))
        except Exception:
            return TransferResult.CurrencyExchangFaillure

    sender_result = sender_balance - sender_subtract
    receiver_result = receiver_balance + receiver_add


    sender.balance = sender_result.into()
    receiver.balance = receiver_result.into()

    transfer = Model(sender=sender, receiver=receiver, rate=rate, amount=amount.into())

    if Model is Payment:
        sender.save()
        receiver.save()

    transfer.save()

    return TransferResult.Ok

def make_payment(request, sender: Account, receiver: Account, amount_str: CurrencyAmount):
    return make_transfer(request, sender, receiver, amount_str, Payment)


def make_request(request, sender: Account, receiver: Account, amount_str: CurrencyAmount):
    return make_transfer(request, sender, receiver, amount_str, Request)




@login_required
def make_tranfer(request, transfer_type):
    if request.method == "GET":
        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type})

    if request.method != "POST":
        return HttpResponseForbidden()

    form = TransferForm(request.POST, user=request.user)
    form_invalid = not form.is_valid()
    if form_invalid:
        exception = (list(form.errors.as_data().values())[0][0]).messages[0]
        messages.error(request, exception)

        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type, "form": form})
    


    form_func = form.get_payment_data if transfer_type == "payment" else form.get_request_data
    transfer_func = make_payment if transfer_type == "payment" else make_request


    sender, receiver, amount = form_func()

    result = transfer_func(request, sender, receiver, amount)


    if result != TransferResult.Ok:
        messages.error(request, result.value)
        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type, "form": form})


    return redirect("home")


@login_required
def view_payments(request):
    account = request.user


    payments = Payment.objects.filter( Q(sender=account) | Q(receiver=account) ).order_by("-date")



    for payment in payments:
        payment.incoming = payment.receiver == account




    return render(request, "payapp/payments.html", {'payments': payments} )

@login_required
def view_requests(request):
    return render(request, "payapp/requests.html")










