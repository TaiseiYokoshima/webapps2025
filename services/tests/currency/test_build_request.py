from utils.currency import CurrencyAmount
from ...currency import build_request
import services.currency as glob
from utils.test_utils import RequestBuilderBase

class TestBuildRequest(RequestBuilderBase):
    def assert_message(self, exception, messages, request, source, target, amount, *args, **kwargs):
        if isinstance(messages, str):
            self.assertRaisesMessage(exception, messages, build_request, request, source, target, amount, *args, **kwargs )
            return

        if not isinstance(messages, list):
            raise Exception("Not a str or list of str")


        try:
            build_request(request, source, target, amount, *args, **kwargs)
        except exception as e:
            msg = str(e)
            self.assertTrue(msg in messages)



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

        messages = ["Cannot convert 0.00 " + source, CurrencyAmount.str_parse_error_msg]
        amounts = [".12.01", "-12.00", "12.0", "12.", "12", ".12", "12.111", "012.12", ".", "..", "...", "....", "00.00", "0.00", "0", "0.", "12.99999"]

        for amount in amounts:
            self.assert_message(ValueError, messages, request, source, target, amount)


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


    def test_https_url(self):
        source = "USD"
        target = "EUR"
        amount = "12.01"
        request = self.create_request_is_secure()

        url = build_request(request, source, target, amount)
        
        self.assertTrue(url.startswith("https://"))


    def test_http_url(self):
        source = "USD"
        target = "EUR"
        amount = "12.01"
        request = self.create_request_not_secure()

        url = build_request(request, source, target, amount)
        
        self.assertTrue(url.startswith("http://"))


    def test_external_api(self):
        source = "USD"
        target = "EUR"
        amount = "12.01"
        glob.external_api_url = "example.com"
        request = self.create_request()

            
        url = build_request(request, source, target, amount)


        self.assertTrue(url.startswith("https://" + glob.external_api_url))








































