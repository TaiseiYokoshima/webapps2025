from decimal import Decimal
from enum import Enum
from services.currency import CurrencyAmount, call_conversion_api
from django.db import transaction


from typing import Union, Type

from accounts.models import Account
from .models import Payment
from .models import Request



class TransferResult(Enum):
    Ok = "success",
    InsufficientFunds = "Failed to make payment due to insufficient funds",
    CurrencyExchangFaillure = "Server error due to currency conversion",
    InvalidStringValueForAmount = "Invalid string value for currency amount",
    TransactionFailure = "Server error due to transaction failure"


@transaction.atomic()
def make_transfer(request, sender: Account, receiver: Account, amount_str: str, Model: Union[Type[Payment], Type[Request]]) -> TransferResult:
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

    if (sender.balance < amount.into()):
        return TransferResult.InsufficientFunds

    if (source != target):
        try:
            result_json = call_conversion_api(request, source, target, amount_str)
            receiver_add = CurrencyAmount(result_json["amount"])
            rate = CurrencyAmount(Decimal(result_json["amount"]))
        except Exception:
            return TransferResult.CurrencyExchangFaillure

    sender_result = sender_balance - sender_subtract
    receiver_result = receiver_balance + receiver_add


    sender.balance = sender_result.into()
    receiver.balance = receiver_result.into()

    transfer = Model(sender=sender, receiver=receiver, rate=rate, amount=Decimal(amount))

    if Model is Payment:
        sender.save()
        receiver.save()

    transfer.save()

    return TransferResult.Ok

def make_payment(request, sender: Account, receiver: Account, amount_str: str):
    return make_transfer(request, sender, receiver, amount_str, Payment)


def make_request(request, sender: Account, receiver: Account, amount_str: str):
    return make_transfer(request, sender, receiver, amount_str, Request)
