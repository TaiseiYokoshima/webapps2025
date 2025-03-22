from django.test import TestCase
from django.urls import reverse


from urllib.parse import quote
from http import HTTPStatus


from .views import rates


from utils.currency import CurrencyAmount


class TestConversionEndPoint(TestCase):
    def make_request(self, source, target, amount):
        amount = quote(str(amount))
        return self.client.get(reverse('convert', args=[source, target, amount]))

    def test_invalid_currency(self):
        invalid = "haha"
        amount = 12.01
        source = target = invalid
        
        response = self.make_request(source, target, amount)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.content.decode(), "Unsupported currency")


    def test_same_currency(self):
        currency = "USD"
        amount = 12.01
        source = target = currency
        
        response = self.make_request(source, target, amount)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.content.decode(), "Cannot convert to the same currency")

    def test_invalid_amounts(self):
        source = "GBP"
        target = "USD"
        amounts = ["1j", "12._", "12.1;", ".0;", ]
        amounts = ["0", "00000000", ".0", ".00", ".000000000000", "0.", "000000000000.", "000000.0000000", "01.00", "0.00", "-12.00", "012.00"]

        for amount in amounts:
            response = self.make_request(source, target, amount)
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            
            err_msg = response.content.decode()
            check = err_msg == CurrencyAmount.str_parse_error_msg or err_msg == "Cannot convert 0.00 " + source
            self.assertTrue(check)


    def test_valid_amounts(self):
        source = "GBP"
        target = "USD"
        amounts = ["12.11", "0.12", "0.01"]
        
        for amount in amounts:
            response = self.make_request(source, target, amount)
            self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_conversion(self):
        amounts = ["1.00", "129.39"]
        for source, dic in rates.items():
            for target, rate in dic.items():
                for amount in amounts:
                    response = self.make_request(source, target, str(amount))
                    self.assertEqual(response.status_code, HTTPStatus.OK)

                    


                    result = response.json()
                    amount_str: str = result["amount"]
                    rate_str: str = result["rate"]

                    self.assertEqual(rate_str, str(rate))


                    calculated = CurrencyAmount(amount) * CurrencyAmount(rate)
                    calculated = str(calculated.into())

                    self.assertEqual(amount_str, calculated)


