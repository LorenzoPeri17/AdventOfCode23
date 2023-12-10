from Pr7 import *

if __name__ == "__main__":
    
    test_input = 'Pr7_test.txt'
    problem_input = 'Pr7_input.txt'

    test = HandList.from_file(test_input, sort = True)
    test_hand_str = [h.hand_str() for h in test]
    test_points = [h.points for h in test]
    test_rank = [h.rank for h in test]

    test_total = test.get_total()

    assert test_hand_str == ['32T3K', 'KTJJT', 'KK677', 'T55J5', 'QQQJA']
    assert test_points == [Point.ONE_PAIR, Point.TWO_PAIRS, Point.TWO_PAIRS, Point.THREE_A_KIND, Point.THREE_A_KIND]
    assert test_rank == [1, 2, 3, 4, 5]
    assert test_total == 6440

    hands = HandList.from_file(problem_input, sort = True)

    print(hands.get_total())


