from Pr8 import *

if __name__ == '__main__':

    test_file_3 = 'Pr8_test_3.txt'
    input_file  = 'Pr8_input.txt'

    test_3 = NodeGraph.from_file(test_file_3)
    steps_3 = test_3.walk_simultaneous_paths_lmc()
    # steps_3 = test_3.walk_simultaneous_paths_iter()

    assert steps_3 == 6, f'Expected 6, got {steps_3}'

    input_graph = NodeGraph.from_file(input_file)
    steps = input_graph.walk_simultaneous_paths_lmc()
    # steps = input_graph.walk_simultaneous_paths_iter()

    print(f'Part 2: {steps}')