from django.test import Client





from .forms import RegisterForm

from .views import register_user_from_form



from utils.test_utils import LiveServerBase

import services.currency as glob

from requests.exceptions import ConnectTimeout



from services.currency import ConversionAPIError


from accounts.models import Account


from decimal import Decimal


from utils.currency import CurrencyAmount
from conversion.views import rates



from http import HTTPStatus



class TestHandleCurrencyChoice(LiveServerBase):
    def setUp(self):
        super().setUp()
        password = "!123123Jj"
        form_data = {
            "email": "taisei@test.com",
            "password1": password,
            "password2": password,
            "currency": "EUR"
        }

        form: RegisterForm = RegisterForm(data=form_data)

        form.is_valid()

        self.form = form


    def test_handle_currency_choice_external_api(self):
        glob.external_api_url = "example.com"
        request = self.create_request_not_secure()
        
        with self.assertRaises(ConversionAPIError):
            register_user_from_form(request, self.form)

        glob.external_api_url = "12.1.1.1"
        with self.assertRaises(ConnectTimeout):
            register_user_from_form(request, self.form)


    def test_handle_currency_choice_internal_api(self):
        request = self.create_request_not_secure()
        user = register_user_from_form(request, self.form)
        self.assertTrue(isinstance(user, Account))


    def test_currency_conversions(self):
        request = self.create_request_not_secure()
        user = register_user_from_form(request, self.form)
        balance = user.balance


        
        source = "GBP"
        target = self.form.cleaned_data["currency"]
        rate = rates[source][target]


        amount = Account.get_default("balance")

        calculated = (CurrencyAmount(amount) * CurrencyAmount(rate)).into()
        calculated =  Decimal(calculated)


        self.assertEqual(balance, calculated)


        user = Account.objects.get(email__exact=self.form.cleaned_data["email"])
        balance = user.balance

        self.assertEqual(balance, calculated)



class TestRegisterEndPoint(LiveServerBase):
    def setUp(self):
        self.client = Client()



    def make_get_request(self):
        response = self.client.get("/register/")
        self.csrf_token = getattr(response, "cookies")["csrftoken"].value
        self.password =  "!123123Jj"
        self.form_data = {
            "csrfmiddlewaretoken": self.csrf_token, 
            "email": "taisei@icloud.com",
            "currency": "EUR",
            "password1": self.password,
            "password2": self.password
        }



        return response


    def test_register(self):
        self.make_get_request()
        self.client.post("/register/", self.form_data, headers={"Referrer": self.live_server_url + "/register/"})
        Account.objects.get(email__exact="taisei@icloud.com")
        self.assertTrue("_auth_user_id" in self.client.session)


    def test_external_api_ip(self):
        response = self.make_get_request()
        glob.external_api_url = "12.1.1.1" 
        response = self.client.post("/register/", self.form_data, headers={"Referrer": self.live_server_url + "/register/"})
        self.assertEqual(getattr(response,"status_code"), HTTPStatus.INTERNAL_SERVER_ERROR)

        with self.assertRaises(getattr(Account, "DoesNotExist")):
            Account.objects.get(email__exact="taisei@icloud.com")



    def test_external_api_domain(self):
        response = self.make_get_request()
        glob.external_api_url = "example.com" 
        response = self.client.post("/register/", self.form_data, headers={"Referrer": self.live_server_url + "/register/"})
        self.assertEqual(getattr(response,"status_code"), HTTPStatus.INTERNAL_SERVER_ERROR)

        with self.assertRaises(getattr(Account, "DoesNotExist")):
            Account.objects.get(email__exact="taisei@icloud.com")
























        




