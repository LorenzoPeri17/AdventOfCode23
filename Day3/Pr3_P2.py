from Pr3 import *

if __name__ == "__main__":
    
    test_input = 'Pr3_test.txt'
    problem_input = 'Pr3_input.txt'

    test = Schematic.from_file(test_input)

    test_gears = test.find_gears()
    test_gear_ratios = [ gear.get_gear_ratio() for gear in test_gears ]

    print([g.value for g in test_gears])
    print([(g.row, g.col) for g in test_gears])
    print([g.adj for g in test_gears])
    print([[n.value for n in g.adjacency_list] for g in test_gears ])

    assert len(test_gears) == 2
    assert test_gear_ratios == [16345, 451490], f'gear ratios: {test_gear_ratios}'
    assert sum(test_gear_ratios) == 467835

    schematic = Schematic.from_file(problem_input)

    gears = schematic.find_gears()
    gear_ratios = [ gear.get_gear_ratio() for gear in gears ]

    print(sum(gear_ratios))