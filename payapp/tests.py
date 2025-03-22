from django.test import TestCase

from accounts.models import Account

from utils.test_utils import LiveServerBase, RequestBuilderBase

from payapp.views import make_payment, make_request, TransferResult



class TestMakePayment(LiveServerBase):

    def setUp(self):
        super().setUp()
        password = "123"
        self.sender = Account.objects.create(email="john@example.com", password=password)
        # self.receiver = Account.objects.create(email="alex@example.com", password=password, currency="EUR")
        self.receiver = Account.objects.create(email="alex@example.com", password=password)

        self.sender.save()
        self.receiver.save()


    def test_valid(self):
        request = self.create_request_not_secure()
        sender = self.sender
        receiver = self.receiver
        amount = "10050.00"
        result: TransferResult = make_payment(request, sender, receiver, amount)
        account = Account.objects.get(email__exact="alex@example.com")

