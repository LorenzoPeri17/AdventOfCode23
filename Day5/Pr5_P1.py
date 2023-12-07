from Pr5 import *

if __name__ == "__main__":
    
    test_input = 'Pr5_test.txt'
    problem_input = 'Pr5_input.txt'

    test = Almanac.from_file(test_input)

    seeds_to_soil = [test.walk(s, 'seed', 'soil') for s in test.seeds]
    seeds_to_location = [test.walk(s, 'seed', 'location') for s in test.seeds]

    print(test.seeds)
    assert seeds_to_soil == [81, 14, 57, 13], f'seeds_to_soil: {seeds_to_soil}'
    assert seeds_to_location == [82, 43, 86, 35], f'seeds_to_location: {seeds_to_location}'
    assert min(seeds_to_location)  == 35

    almanac = Almanac.from_file(problem_input)

    seeds_to_location = [almanac.walk(s, 'seed', 'location') for s in almanac.seeds]

    print(min(seeds_to_location))