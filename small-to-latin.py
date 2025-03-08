def number_to_latin(n):
    # Basic numbers and tens
    numbers = {
        1: "ūnus", 2: "duo", 3: "trēs", 4: "quattuor", 5: "quīnque",
        6: "sex", 7: "septem", 8: "octō", 9: "novem", 10: "decem",
        20: "vīgintī", 30: "trīgintā", 40: "quadrāgintā", 50: "quīnquāgintā",
        60: "sexāgintā", 70: "septuāgintā", 80: "octōgintā", 90: "nōnāgintā",
        100: "centum"
    }

    # Special cases for 18, 19, ..., 98, 99
    special_cases = {
        18: "duodēvīgintī", 19: "ūndēvīgintī",
        28: "duodētrīgintā", 29: "ūndētrīgintā",
        38: "duodēquadrāgintā", 39: "ūndēquadrāgintā",
        48: "duodēquīnquāgintā", 49: "ūndēquīnquāgintā",
        58: "duodēsexāgintā", 59: "ūndēsexāgintā",
        68: "duodēseptuāgintā", 69: "ūndēseptuāgintā",
        78: "duodēoctōgintā", 79: "ūndēoctōgintā",
        88: "duodēnōnāgintā", 89: "ūndēnōnāgintā",
        98: "duodēcentum", 99: "ūndēcentum"
    }

    # Check if the number is in the special cases
    if n in special_cases:
        return special_cases[n]

    # If the number is a simple base or ten, return it directly
    if n in numbers:
        return numbers[n]

    # Otherwise, construct the number from tens and units
    tens, ones = divmod(n, 10)
    tens *= 10
    latin_number = numbers[tens]
    if ones > 0:
        latin_number += " " + numbers[ones]

    return latin_number

# Test the function with a range of numbers
print([number_to_latin(n) for n in [79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]])


