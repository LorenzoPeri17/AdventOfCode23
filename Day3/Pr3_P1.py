from Pr3 import *

if __name__ == "__main__":
    
    test_input = 'Pr3_test.txt'
    problem_input = 'Pr3_input.txt'

    test = Schematic.from_file(test_input)

    # print('bad numbers: ', [number.value for number in test.bad_numbers])
    assert len(test.bad_numbers)+len(test.part_numbers) == 10
    assert len(test.bad_numbers) == 2
    assert sum(number.value for number in test.part_numbers) == 4361

    schematic = Schematic.from_file(problem_input)

    print(sum(number.value for number in schematic.part_numbers))