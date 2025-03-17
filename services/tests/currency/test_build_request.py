from django.test import TestCase, RequestFactory


from ...currency import build_request


import services.currency as glob



class TestBuildRequest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()


    def create_request(self):
        request = self.factory.get("/")
        request.get_host = lambda: "127.0.0.1:8000"

        return request

    def create_request_is_secure(self):
        request = self.create_request()
        request.is_secure = lambda: True  
        return request

    def create_request_not_secure(self):
        request = self.create_request()
        request.is_secure = lambda: False
        return request


    def assert_message(self, request, source, target, amount, exception, message):
        with self.assertRaisesMessage(exception, message):
            build_request(request, source, target, amount)



    def test_invalid_currencies(self):
        source = "kjfjl"
        target = "lksdjf"
        amount = "12.01"
        request = self.create_request_not_secure()


        self.assert_message(request, source, target, amount, ValueError, "Unsupported currency")


        source = "USD"
        target = "USD"

        self.assert_message(request, source, target, amount, ValueError, "Cannot convert to the same currency")

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
            self.assert_message(request, source, target, amount, ValueError, "Invalid value for amount")


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
        glob.base_url = "example.com"
        request = self.create_request()

            
        url = build_request(request, source, target, amount)


        self.assertTrue(url.startswith("https://" + glob.base_url))

    def tearDown(self) -> None:
        glob.base_url = None







































