from django.test import TestCase

from ..currency import invalid_amount_string, calculate_conversion_from_string, set_decimal_places

from decimal import Decimal, localcontext



class TestCurrency(TestCase):

    def test_invalid_amount_string(self):

        amounts = ["01.00", "0.0.0", "0", "12", "12.0", "-12.00"]

        for amount in amounts:
            result = invalid_amount_string(amount)
            self.assertTrue(result)


    def test_set_decimal_places(self):
        with localcontext() as ctx:
            ctx.prec = 50 + 18

            string = str("1" * 25 + "." + "9" * 18)
            value = Decimal(string)
            result = str(set_decimal_places(value, 2))

            decimals = result.split(".")

            self.assertEqual(2, len(decimals))
            decimals = decimals[1]

            self.assertEqual(2, len(decimals))
    

    def test_calculate_conversion_from_string(self):
        amount = "111.11"
        rate = 0.233
        result = "25.88"

        self.assertEqual(result, calculate_conversion_from_string(amount, rate))



        

        
        
        





        

        


        

            





        


        


