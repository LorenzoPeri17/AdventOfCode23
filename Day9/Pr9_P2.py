from Pr9 import *

if __name__ == "__main__":
    
    test_input = 'Pr9_test.txt'
    problem_input = 'Pr9_input.txt'

    test = ReadingList.from_file(test_input)
    extrapolated = test.extrapolate_left()

    assert extrapolated == [-3, 0, 5], extrapolated
    assert sum(extrapolated) == 2
    
    readings = ReadingList.from_file(problem_input)

    print(sum(readings.extrapolate_left()))


