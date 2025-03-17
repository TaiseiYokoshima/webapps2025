from decimal import Decimal, localcontext, ROUND_DOWN


def invalid_amount_string(amount: str) -> bool:
    parse_amount = amount.split(".")

    if (
            len(parse_amount) != 2 or 
            parse_amount[0] == "" or 
            parse_amount[1] == "" or 
            len(parse_amount[1]) != 2
        ):
        return True

    
    for char in parse_amount[0]:
        if not char.isdigit():
            return True

     
    for char in parse_amount[1]:
        if not char.isdigit():
            return True



    integer = parse_amount[0]

    if (integer != str(int(integer))):
        return True

    if (integer != "0" and integer.startswith("0")):
        return True



    return False




def set_decimal_places(value: Decimal, places: int) -> Decimal:
    string = str("1." + "0" * places)
    quantizer = Decimal(string)
    return value.quantize(quantizer, rounding=ROUND_DOWN)



def calculate_conversion_from_string(amount: str, rate: float) -> str:
    with localcontext() as ctx:
        ctx.prec = 68
        result  = Decimal(amount) * Decimal(rate)
        return str(set_decimal_places(result, 2))



