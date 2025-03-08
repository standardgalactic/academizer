def arabic_to_cistercian(num):
    # Dictionary for Cistercian digits
    cistercian_units = {
        0: '\uEBA0', 1: '\uEBA1', 2: '\uEBA2', 3: '\uEBA3', 4: '\uEBA4',
        5: '\uEBA5', 6: '\uEBA6', 7: '\uEBA7', 8: '\uEBA8', 9: '\uEBA9'
    }
    cistercian_tens = {
        1: '\uEBB1', 2: '\uEBB2', 3: '\uEBB3', 4: '\uEBB4',
        5: '\uEBB5', 6: '\uEBB6', 7: '\uEBB7', 8: '\uEBB8', 9: '\uEBB9'
    }
    cistercian_hundreds = {
        1: '\uEBC1', 2: '\uEBC2', 3: '\uEBC3', 4: '\uEBC4',
        5: '\uEBC5', 6: '\uEBC6', 7: '\uEBC7', 8: '\uEBC8', 9: '\uEBC9'
    }
    cistercian_thousands = {
        1: '\uEBD1', 2: '\uEBD2', 3: '\uEBD3', 4: '\uEBD4',
        5: '\uEBD5', 6: '\uEBD6', 7: '\uEBD7', 8: '\uEBD8', 9: '\uEBD9'
    }

    # Splitting the number into thousands, hundreds, tens, and units
    units = num % 10
    tens = (num // 10) % 10
    hundreds = (num // 100) % 10
    thousands = (num // 1000) % 10

    # Assembling the Cistercian numeral
    return (cistercian_thousands.get(thousands, '') +
            cistercian_hundreds.get(hundreds, '') +
            cistercian_tens.get(tens, '') +
            cistercian_units.get(units, ''))

# Example usage:
result = arabic_to_cistercian(1234)
print(result)  # Should print the Cistercian numerals for 1234
