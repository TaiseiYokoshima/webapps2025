from django.test import TestCase

from accounts.models import Account
from .models import Transfer

# class TransactionTestCase(TestCase):
#     def setUp(self):
#         password = "123"
#         self.sender = Account.objects.create(email="john@example.com", password=password)
#         self.receiver = Account.objects.create(email="alex@example.com", password=password)
#         self.transaction = Transfer.objects.create(sender=self.sender, receiver=self.receiver, amount=100)
#
#
#
#
#     def test_transaction_creation(self):
#         self.assertEqual(self.transaction.amount, 100)
#
#     def test_sender_and_receiver(self):
#         self.assertEqual(self.transaction.sender.email, "john@example.com")
#         self.assertEqual(self.transaction.receiver.email, "alex@example.com")

