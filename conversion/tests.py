from django.test import TestCase

from django.urls import reverse

from .views import rates, calculate_conversion


from http import HTTPStatus


from urllib.parse import quote

# Create your tests here.

class ConversionTestCase(TestCase):
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
        amounts = ["0", "00000000", ".0", ".00", ".000000000000", "0.", "000000000000.", "000000.0000000"]

        for amount in amounts:
            response = self.make_request(source, target, amount)
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(response.content.decode(), "Invalid value for amount")


    def test_valid_amounts(self):
        source = "GBP"
        target = "USD"
        amounts = ["000000012.", "0000000012.00000012", "00000012.", "0000000012"]
        amounts += ["12.0000001", "12.1", "12.00000012"]
        
        for amount in amounts:
            response = self.make_request(source, target, amount)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    

    def test_conversion(self):
        amounts = ["1.0", "129.0000000", "00000012.5"]
        for source, dic in rates.items():
            for target, rate in dic.items():
                for amount in amounts:
                    response = self.make_request(source, target, amount)
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                    result = response.json()["result"]
                    calculated = calculate_conversion(float(amount), rate)
                    self.assertEqual(result, calculated)



