from Pr9 import *

if __name__ == "__main__":
    
    test_input = 'Pr9_test.txt'
    problem_input = 'Pr9_input.txt'

    test = ReadingList.from_file(test_input)
    extrapolated = test.extrapolate()

    assert extrapolated == [18, 28, 68]
    assert sum(extrapolated) == 114
    
    readings = ReadingList.from_file(problem_input)

    print(sum(readings.extrapolate()))



