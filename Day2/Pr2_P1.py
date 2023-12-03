from Pr2 import *

if __name__ == '__main__':

    test_input = 'Pr2_test.txt'
    problem_input = 'Pr2_input.txt'

    tests = get_Games_from_file(test_input)

    possible_games_test = [game for game in tests if game.is_possible()]
    assert len(possible_games_test) == 3
    assert sum(game.number for game in possible_games_test) == 8

    games = get_Games_from_file(problem_input)

    possible_games = [game for game in games if game.is_possible()]

    print('Possible games: ', [game.number for game in possible_games])
    print('Result: ', sum(game.number for game in possible_games))
