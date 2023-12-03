import re, os

#!------------------------- Disclaimer -------------------------!#
# This solution is a terrible hack
# but oh well, it works for the given input
# \shrug/
#!------------------------- Disclaimer -------------------------!#


numeric_pattern = re.compile(r'\d')
numeric_and_spelled_pattern = re.compile(r'\d|one|two|three|four|five|six|seven|eight|nine|(?<=o)ne|(?<=t)wo|(?<=t)hree|(?<=e)ight|(?<=n)ine')

spell_to_digit = {
    'one': '1',
    'ne': '1', # handle the collision with the last 'o' of other numbers
    'two': '2',
    'wo': '2', # handle the collision with the last 't' of other numbers
    'three': '3',
    'hree': '3', # handle the collision with the last 't' of other numbers
    'four': '4',
    'five': '5',
    'six' : '6',
    'seven': '7',
    'eight': '8',
    'ight': '8', # handle the collision with the last 'e' of other numbers
    'nine': '9',
    'ine': '9' # handle the collision with the last 'n' of 'seven'
}


problem_input = 'Pr1_input.txt'

test_input_1 = 'Pr1_test1.txt'
test_input_2 = 'Pr1_test2.txt'

def find_coordinate(filename, *, parse_spelled_numbers):

    if parse_spelled_numbers:
        _pattern = numeric_and_spelled_pattern
    else:
        _pattern = numeric_pattern

    total_sum = 0

    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath) as f:
        lines = f.readlines()

        for line in lines:
            digits = _pattern.findall(line)
            # digits is a list of strings

            if parse_spelled_numbers:
                # convert spelled numbers to digits
                digits = [spell_to_digit[digit] if digit in spell_to_digit.keys() else digit for digit in digits]
                
            # concatenate first and last digits and convert to int
            number = int(digits[0] + digits[-1]) 
            
            total_sum += number

    return total_sum


# test1 = find_coordinate(test_input_1, parse_spelled_numbers=False)
# assert test1  == 142
# print('Test 1 passed')

test2 = find_coordinate(test_input_2, parse_spelled_numbers=True)
assert test2  == 281
print('Test 2 passed')

# result = find_coordinate(problem_input, parse_spelled_numbers=False)
# print('Result without parsing spelling: ', result)

result = find_coordinate(problem_input, parse_spelled_numbers=True)
print('Result with parsing spelling: ', result)