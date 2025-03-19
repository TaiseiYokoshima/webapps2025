

from ...currency import build_request, call_conversion_api, ConversionAPIError


import services.currency as glob

from requests.exceptions import ConnectTimeout


from conversion.views import rates, CurrencyAmount


from utils.test_utils import LiveServerBase 


class TestCallConversionAPI(LiveServerBase):
    def assert_message(self, exception, message, *args, **kwargs):
        self.assertRaisesMessage(exception, message, call_conversion_api, *args, **kwargs)

    def test_invalid_currencies(self):
        source = "kjfjl"
        target = "lksdjf"
        amount = "12.01"
        request = self.create_request_not_secure()


        self.assert_message(ValueError, "Unsupported currency", request, source, target, amount)


        source = "USD"
        target = "USD"

        self.assert_message(ValueError, "Cannot convert to the same currency", request, source, target, amount)

    def test_valid_currencies(self):
        source = "USD"
        target = "GBP"
        amount = "12.01"
        request = self.create_request_not_secure()

        try:
            build_request(request, source, target, amount)
        except ValueError as e:
            self.fail(f"Test failed due to exception raised:\n{e}")


    def test_invalid_amounts(self):
        source = "USD"
        target = "EUR"
        request = self.create_request_not_secure()

        amounts = [".12.01", "-12.00", "12.0", "12.", "12", ".12", "12.111", "012.12", ".", "..", "...", "....", "00.00", "0.00", "0", "0.", "12.99999"]

        for amount in amounts:
            try:
                call_conversion_api(request, source, target, amount)
            except ValueError as e:
                msg = str(e)
                check = msg ==  "Invalid string for a currency amount" or msg == "Cannot convert 0.00 " + source
                self.assertTrue(check)
                




    def test_valid_amounts(self):
        source = "USD"
        target = "EUR"
        request = self.create_request_not_secure()

        amounts = ["12.01", "12.10", "2.00", "111111.01"]

        for amount in amounts:
            try:
                build_request(request, source, target, amount)
            except ValueError as e:
                self.fail(f"Test failed due to exception raised:\n{e}")


    
    def test_conversion_results(self):
        source = "USD"
        target = "EUR"
        rate = rates[source][target]
        request = self.create_request_not_secure()

        amounts = ["12.01", "12.10", "2.00", "111111.01"]

        for amount in amounts:
            calculated = CurrencyAmount(amount) * CurrencyAmount(rate)
            calculated = str(calculated.into())
            result = call_conversion_api(request, source, target, amount)
            result = str(result)
            self.assertEqual(result, calculated)


    def test_external_api_with_domain(self):
        source = "USD"
        target = "EUR"
        amount = "12.01"
        glob.external_api_url = "example.com"
        request = self.create_request()

        with self.assertRaises(ConversionAPIError):
            call_conversion_api(request, source, target, amount)

    def test_external_api_with_ip(self):
        source = "USD"
        target = "EUR"
        amount = "12.01"
        glob.external_api_url = "12.1.1.1"
        request = self.create_request()


        with self.assertRaises(ConnectTimeout):
            call_conversion_api(request, source, target, amount)
            








































