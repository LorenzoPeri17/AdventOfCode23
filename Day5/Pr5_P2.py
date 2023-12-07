from Pr5 import *
from tqdm import tqdm

if __name__ == "__main__":
    
    test_input = 'Pr5_test.txt'
    problem_input = 'Pr5_input.txt'

    a = np.empty(10, dtype=np.int64)
    a[0:3] = np.arange(3)

    test = Almanac.from_file(test_input, seeds_are_ranges=True)

    assert len(test.seeds) == 27
    assert np.allclose(test.seeds, np.concatenate([79+np.arange(14), 55 + np.arange(13)]))

    # seeds_to_soil = [test.walk(s, 'seed', 'soil') for s in test.seeds]
    # seeds_to_location = [test.walk(s, 'seed', 'location') for s in test.seeds]
    # seeds_to_location = [test.walk_seed_loc(s) for s in test.seeds]
    seeds_to_location = test.walk_seed_loc_ranges()
    # print(seeds_to_location)

    # print(test.seeds)
    # assert seeds_to_soil == [81, 14, 57, 13], f'seeds_to_soil: {seeds_to_soil}'
    # assert seeds_to_location == [82, 43, 86, 35], f'seeds_to_location: {seeds_to_location}'
    assert seeds_to_location.min()  == 46, f'seeds_to_location: {seeds_to_location.min()}'

    almanac = Almanac.from_file(problem_input, seeds_are_ranges=True)

    # seeds_to_location = [almanac.walk(s, 'seed', 'location') for s in almanac.seeds]
    # seeds_to_location = []
    # seed_number = len(almanac.seeds)
    # for s in tqdm(almanac.seeds):
    #     # print(f'{i+1}/{seed_number} seeds processed', end = '\r')
    #     seeds_to_location.append(almanac.walk(s, 'seed', 'location'))

    seeds_to_location = almanac.walk_seed_loc_ranges()

    print(seeds_to_location.min())