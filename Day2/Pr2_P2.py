from Pr2 import *

if __name__ == '__main__':

    test_input = 'Pr2_test.txt'
    problem_input = 'Pr2_input.txt'

    tests = get_Games_from_file(test_input)

    powers_test = [game.get_power() for game in tests]
    assert powers_test == [48, 12, 1560, 630, 36]
    assert sum(powers_test) == 2286

    games = get_Games_from_file(problem_input)

    powers = [game.get_power() for game in games]

    print('Result: ', sum(powers))
