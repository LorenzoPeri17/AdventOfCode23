from Pr8 import *
import cProfile, time

if __name__ == '__main__':

    test_file_3 = 'Pr8_test_3.txt'
    input_file  = 'Pr8_input.txt'

    test_3 = NodeGraph.from_file(test_file_3)
    # # steps_3 = test_3.walk_simultaneous_paths()
    steps_3 = test_3.walk_simultaneous_paths_hardstop(hardstop  = 10_000_000)

    assert steps_3 == 6, f'Expected 6, got {steps_3}'

    input_graph = NodeGraph.from_file(input_file)
    # steps = input_graph.walk_simultaneous_paths()
    with cProfile.Profile() as pr:
        start = time.time()
        steps = input_graph.walk_simultaneous_paths_hardstop(hardstop  = 20_000_000)
        tot_time = time.time() - start
        print(f'Part 2: {steps} in {tot_time:.2f} seconds ({steps/tot_time:.0f} iterations/second)')
        pr.print_stats(sort='tottime')