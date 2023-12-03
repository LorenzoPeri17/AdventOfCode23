import re, os
import numpy as np
from typing import List

class PartNumber:
    value        : int
    row          : int
    column_start : int
    column_end   : int

class Symbol:
    value : str
    row   : int
    col   : int
    adj   : int = 0
    adjacency_list : List[PartNumber]

    def __init__(self): 
        # for f..k sake
        # lists are MUTABLE ...
        self.adjacency_list = []

    def get_gear_ratio(self):
        if self.adj == 2:
            return self.adjacency_list[0].value * self.adjacency_list[1].value
        else:
            raise ValueError('Symbol is not a gear')

class Schematic:

    _number_pattern = re.compile(r'\d+')
    _symbol_pattern = re.compile(r'[^\d.\n]')

    def __init__(self, numbers, symbols):
        self.symbols = symbols
        self.part_numbers = []
        self.bad_numbers = []
        self.find_good_numbers(numbers)

    @staticmethod
    def from_file(filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
            numbers = []
            symbols = []
            for i, line in enumerate(lines):
                for m in Schematic._number_pattern.finditer(line):
                    number = PartNumber()
                    number.value = int(m.group())
                    number.row = i
                    number.column_start = m.start()
                    number.column_end = m.end()-1
                    numbers.append(number)
                for m in Schematic._symbol_pattern.finditer(line):
                    symbol = Symbol()
                    symbol.value = m.group()
                    symbol.row = i
                    symbol.col = m.start()
                    symbols.append(symbol)
            return Schematic(numbers, symbols)
        
    @staticmethod
    def _check_adjacent(number, symbol):
        if number.row == symbol.row:
            if number.column_start == symbol.col + 1 or number.column_end == symbol.col - 1:
                return True
        elif number.row == symbol.row + 1 or number.row == symbol.row - 1:
            if number.column_start -1 <= symbol.col <= number.column_end +1:
                return True
        return False
        
    def find_good_numbers(self, numbers):
        for symbol in self.symbols:
            for number in numbers.copy():
                if Schematic._check_adjacent(number, symbol):
                    self.part_numbers.append(number)
                    numbers.remove(number)
                    symbol.adj += 1
                    symbol.adjacency_list.append(number)
        
        self.bad_numbers = numbers
        
    def find_gears(self):
        gears = []
        for symbol in self.symbols:
            if symbol.value == '*' and symbol.adj == 2:
                gears.append(symbol)
        return gears
    