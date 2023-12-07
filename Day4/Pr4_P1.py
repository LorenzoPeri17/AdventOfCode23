from Pr4 import *

if __name__ == "__main__":
    
    test_input = 'Pr4_test.txt'
    problem_input = 'Pr4_input.txt'

    test = Cards_from_file(test_input)

    test_points = [card.get_points() for card in test]

    assert test_points ==[8, 2, 2, 1, 0, 0], f'points: {test_points}'
    assert sum(test_points) == 13

    cards = Cards_from_file(problem_input)

    points = [card.get_points() for card in cards]

    print(sum(points))

