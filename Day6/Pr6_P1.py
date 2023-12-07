from Pr6 import *

if __name__ == "__main__":
    
    test_input = 'Pr6_test.txt'
    problem_input = 'Pr6_input.txt'

    test = Races.from_file(test_input)

    test_win = test.get_winning_numbers()

    assert test_win == [4, 8, 9]
    assert np.prod(test_win) == 288

    races = Races.from_file(problem_input)

    print(np.prod(races.get_winning_numbers()))