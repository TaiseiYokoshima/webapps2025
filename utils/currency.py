from decimal import Decimal, localcontext, Context, ROUND_HALF_EVEN
from typing import Literal

import re


precision = 68
places = 20



ROUND_OPTION = Literal[
        "ROUND_DOWN", "ROUND_UP", "ROUND_HALF_EVEN"
]


class CurrencyAmount(Decimal):
    amount_ctx = Context(prec=precision)

    @staticmethod
    def parse_str_strict(amount: str):
        pattern = r'^(0|[1-9][0-9]*)\.[0-9]{2}$'
        result = re.findall(pattern,amount)
        if len(result) == 0:
            return False

        return True

    str_parse_error_msg = "Invalid string for a currency amount"


    def __new__(cls, value):
        with localcontext(cls.amount_ctx):
            value = cls.amount_ctx.create_decimal(str(value))
            return super().__new__(cls, value)

    
    def __check_type(self, other):
        if not isinstance(other, CurrencyAmount):
            raise TypeError(f"Unsupported operand type: {type(self)} and {type(other)}")

    def __OP(self, other, operation):
        self.__check_type(other)
        with localcontext(self.amount_ctx):
            return CurrencyAmount(operation(Decimal(self), Decimal(other)))

    def __add__(self, other):
        operation = lambda x, y : x + y
        return self.__OP(other, operation)

    def __sub__(self, other):
        operation = lambda x, y : x - y
        return self.__OP(other, operation)

    def __mul__(self, other):
        operation = lambda x, y : x * y
        return self.__OP(other, operation)

    def __truediv__(self, other):
        operation = lambda x, y : x / y
        return self.__OP(other, operation)


    def into(self, rounding: ROUND_OPTION = ROUND_HALF_EVEN) -> Decimal:
        places_str = "1." + "0" * places
        quantizer = Decimal(places_str)
        return Decimal(self).quantize(quantizer, rounding=rounding)

    def to_api_str(self) -> str:
        rounding = ROUND_HALF_EVEN
        places_str = "1.00"
        quantizer = Decimal(places_str)
        return str(Decimal(self).quantize(quantizer, rounding=rounding))


    
    


        

            












