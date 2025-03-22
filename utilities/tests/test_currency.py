from django.test import TestCase


from decimal import ROUND_DOWN, Decimal, localcontext


from ..currency import CurrencyAmount


from conversion.views import rates



class TestCustomDecimalType(TestCase):

    def test_reject_strings_for_constructor(self):
        amounts = [
            "01.00", "0.0.0", "0", "12", "12.0", "-12.00", "0.0", "1.0", "1.", ".1", ".10", ".99" 
        ]

        for amount in amounts:
            self.assertRaisesMessage(ValueError, "Invalid string", CurrencyAmount, amount)
                # CurrencyAmount(amount)



    def test_accept_strings_for_constructor(self):
        amounts = [
            "1.00", "0.00", "12.00", "12.99", "111111111111111.99",
        ]

        for amount in amounts:
                CurrencyAmount(amount)

    def test_currency_conversions(self):
        source = "GBP"
        target = "EUR"
        amount = CurrencyAmount("750.00")
        rate = CurrencyAmount(rates[source][target])
        

        result = (amount * rate)

        amount = "750.00"
        rate= rates[source][target]

        calculated = None


        with localcontext() as ctx:
            ctx.prec = CurrencyAmount.precision
            calculated = Decimal(amount) *  Decimal(str(rate))

        self.assertEqual(result, calculated)

        result = result.into()
        calculated = calculated.quantize(Decimal("0.00"), rounding=ROUND_DOWN)

        self.assertEqual(result, calculated)
    














        











        

        




        

        
        
        





        

        


        

            





        


        


