from django.http import HttpResponseBadRequest

from django.http import JsonResponse
from django.views.decorators.http import require_GET


from utils.currency import invalid_amount_string, calculate_conversion_from_string



from_gbp = { "EUR": 1.19, "USD": 1.29 }

from_eur = { "GBP": 0.84, "USD": 1.09 }

from_usd = { "GBP": 0.77, "EUR": 0.92 }


rates = {
        "GBP": from_gbp,
        "EUR": from_eur,
        "USD": from_usd
        }


@require_GET
def convert(request, source, target, amount):

    source = source.upper()
    target = target.upper()

    if source not in rates or target not in rates:
        return HttpResponseBadRequest("Unsupported currency")

    if source == target:
        return HttpResponseBadRequest("Cannot convert to the same currency")

    if (invalid_amount_string(amount)):
        return HttpResponseBadRequest("Invalid value for amount")

    if (float(amount) == 0):
        return HttpResponseBadRequest("Invalid value for amount")

    rate = rates[source][target]
    result = calculate_conversion_from_string(amount, rate)


    return JsonResponse({'result': result})

    







