from Pr6 import *

if __name__ == "__main__":
    
    test_input = 'Pr6_test.txt'
    problem_input = 'Pr6_input.txt'

    test = Race.from_file_no_spaces(test_input)

    test_win = test.get_winning_numbers()

    assert test_win == 71503

    race = Race.from_file_no_spaces(problem_input)

    print(race.get_winning_numbers())