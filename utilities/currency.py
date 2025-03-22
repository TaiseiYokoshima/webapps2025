from decimal import Decimal, localcontext, ROUND_DOWN, Context
from typing import Literal

import re




ROUND_OPTION = Literal[
        "ROUND_DOWN", "ROUND_UP", 
]


class CurrencyAmount(Decimal):
    precision = 68
    amount_ctx = Context(prec=precision)

    str_parse_error_msg = "Invalid string for a currency amount"



    @classmethod
    def parse_str(cls, amount: str):
        pattern = r'^(0|[1-9][0-9]*)\.[0-9]{2}$'
        result = re.findall(pattern,amount)
        if len(result) == 0:
            raise ValueError(cls.str_parse_error_msg)

    def __new__(cls, input: float | str | Decimal | int):
        if isinstance(input, str):
            cls.parse_str(input)

        return super().__new__(cls, str(input))

    
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


    def into(self, rounding: ROUND_OPTION = ROUND_DOWN) -> Decimal:
        places = "1.00"
        quantizer = Decimal(places)
        return Decimal(self).quantize(quantizer, rounding=rounding)

    
    


        

            












