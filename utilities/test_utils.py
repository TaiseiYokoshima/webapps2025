from django.test import TestCase, LiveServerTestCase, RequestFactory, Client


import services.currency as glob


class RequestBuilderBase(TestCase):
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
    
    def tearDown(self) -> None:
        glob.external_api_url = None

class LiveServerBase(LiveServerTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.base_url = self.live_server_url

    def create_request(self):
        request = self.factory.get("/")
        request.get_host = lambda: self.live_server_url
        return request

    def create_request_is_secure(self):
        request = self.create_request()
        request.is_secure = lambda: True  
        return request

    def create_request_not_secure(self):
        request = self.create_request()
        request.is_secure = lambda: False
        return request

    def tearDown(self) -> None:
        glob.external_api_url = None

