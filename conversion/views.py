from django.http import HttpResponseBadRequest

from django.http import JsonResponse
from django.views.decorators.http import require_GET



import math

# Create your views here.

from_gbp = { "EUR": 1.19, "USD": 1.29 }

from_eur = { "GBP": 0.84, "USD": 1.09 }

from_usd = { "GBP": 0.77, "EUR": 0.92 }


rates = {
        "GBP": from_gbp,
        "EUR": from_eur,
        "USD": from_usd
        }


def calculate_conversion(amount, rate):
    result = math.floor(amount * rate * 100) / 100
    return float(result)


@require_GET
def convert(request, source, target, amount):
    source = source.upper()
    target = target.upper()

    if source not in rates or target not in rates:
        return HttpResponseBadRequest("Unsupported currency")

    if source == target:
        return HttpResponseBadRequest("Cannot convert to the same currency")


    for char in amount:
        if not char.isdigit() and char != ".":
            return HttpResponseBadRequest("Invalid value for amount")


    # print("\n\ngot: ", amount, end="\n\n")

    try:
        amount = float(int(float(amount) * 100) / 100)
    except ValueError:
        return HttpResponseBadRequest("Invalid value for amount")


    rate = rates[source][target]

    result = calculate_conversion(amount, rate)


    if result == 0:
        return HttpResponseBadRequest("Invalid value for amount")


    return JsonResponse({'result': result})

    







