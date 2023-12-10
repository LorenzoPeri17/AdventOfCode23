from Pr8 import *

if __name__ == '__main__':

    test_file_1 = 'Pr8_test_1.txt'
    test_file_2 = 'Pr8_test_2.txt'
    input_file  = 'Pr8_input.txt'

    test_1 = NodeGraph.from_file(test_file_1)
    steps_1 = test_1.walk_path()

    assert steps_1 == 2

    test_2 = NodeGraph.from_file(test_file_2)
    steps_2 = test_2.walk_path()

    assert steps_2 == 6

    input_graph = NodeGraph.from_file(input_file)
    steps = input_graph.walk_path()

    print(f'Part 1: {steps}')