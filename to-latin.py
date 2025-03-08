def number_to_latin_general(n):
    # Extend mappings to include thousands and hundreds
    numbers = {
        1: "ūnus", 2: "duo", 3: "trēs", 4: "quattuor", 5: "quīnque",
        6: "sex", 7: "septem", 8: "octō", 9: "novem", 10: "decem",
        20: "vīgintī", 30: "trīgintā", 40: "quadrāgintā", 50: "quīnquāgintā",
        60: "sexāgintā", 70: "septuāgintā", 80: "octōgintā", 90: "nōnāgintā",
        100: "centum", 200: "ducentī", 300: "trecentī", 400: "quadringentī",
        500: "quingentī", 600: "sescentī", 700: "septingentī", 800: "octingentī",
        900: "nongentī", 1000: "mīlle"
    }
    
    # Handle thousands separately
    latin_number = ""
    if n >= 1000:
        thousands = n // 1000
        latin_number += numbers[1000] * thousands  # Assuming repetition for simplicity
        n %= 1000
    
    # Hundreds
    if n >= 100:
        hundreds = n // 100 * 100
        latin_number += " " + numbers[hundreds] if hundreds in numbers else ""
        n %= 100
    
    # Special cases for 18, 19, ..., 98, 99 are now generalized in the tens handling
    
    # Tens and ones
    if n > 0:
        if n in numbers:  # Direct match
            latin_number += " " + numbers[n]
        else:  # Construct from tens and ones
            tens, ones = divmod(n, 10)
            tens *= 10
            latin_number += " " + numbers[tens] if tens > 0 else ""
            latin_number += " " + numbers[ones] if ones > 0 else ""
    
    return latin_number.strip()

# Test the enhanced function with a range of numbers including years
[number_to_latin_general(n) for n in [79, 80, 81, 100, 101, 199, 200, 2020, 2021]]

print([number_to_latin_general(n) for n in [1889, 1951, 1921, 1929, 1930, 26, 29, 1903, 1908, 1911, 1922]])

