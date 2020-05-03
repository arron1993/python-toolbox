import argparse

LESS_THAN_TWENTY = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen'
}

LESS_THAN_HUNDRED = {
    1: 'ten',
    2: 'twenty',
    3: 'thirty',
    4: 'forty',
    5: 'fifty',
    6: 'sixty',
    7: 'seventy',
    8: 'eighty',
    9: 'ninety'
}

DIV_BREAKPOINTS = {
    1000000: "million",
    1000: "thousand",
    100: "hundred",
}


def process_number(number, entry_word=None):
    values = []
    for current_breakpoint, word in DIV_BREAKPOINTS.items():
        significant_number = (number // current_breakpoint)
        if significant_number >= 19:
            # The number is between 100 and 20 so it needs further parsing
            # e.g. 33 still needs to be split into thirty + three
            # we recursively call ourself to catch thirty three thousand etc
            values += process_number(significant_number, entry_word=word)
        else:
            if current_breakpoint < 100:
                # we're in the lower numbers now that can just be set
                # without too much work
                values.append(LESS_THAN_HUNDRED[significant_number])
                values.append(word)
            else:
                # we're still a big number but minor unit of the number
                # e.g from earlier we're in the 'three' bit of thirty three
                # thousand
                if significant_number != 0:
                    values.append(LESS_THAN_TWENTY[significant_number])
                    values.append(word)
        number = number % current_breakpoint

    if number < 100:
        # this is just the left over numbers, if we're less than 100 just
        tenths = number // 10
        units = number % 10
        if len(values):
            values.append("and")
        if tenths:
            values.append(LESS_THAN_HUNDRED[tenths])
        if units:
            values.append(LESS_THAN_TWENTY[units])
        if entry_word:
            values.append(entry_word)
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="number", required=True)
    args = parser.parse_args()
    number = int(args.number)
    values = []

    values = process_number(number)

    print(' '.join(values))
    return 0


if __name__ == '__main__':
    main()
