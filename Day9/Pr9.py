import re, os
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from tqdm import tqdm
from enum import Enum, unique

class Reading:

    _meas_pattern = re.compile(r'([-\d]+)')
    _diff_kernel = np.array([1, -1], dtype=np.int64)

    def __init__(self, measurement : np.ndarray[np.int64]) -> None:
        self.measurement = measurement

    def __str__(self) -> str:
        return str(self.measurement)
    
    def extrapolate(self) -> np.int64:
        array = self.measurement
        value = np.int64(0)
        
        while not np.allclose(array, np.zeros_like(array)):

            value += np.int64(array[-1])
            array = np.convolve(array, self._diff_kernel, mode='valid')

        return value
    
    def extrapolate_left(self) -> np.int64:
        array = self.measurement
        value = np.int64(0)
        sign = np.int64(1)

        while not np.allclose(array, np.zeros_like(array)):

            value += np.int64(array[0])*sign
            sign *= -1
            array = np.convolve(array, self._diff_kernel, mode='valid')

        return value
    
    def parse(line : str) -> 'Reading':
        return Reading(np.array([np.int64(x) for x in Reading._meas_pattern.findall(line)], dtype=np.int64))
    

class ReadingList:

    def __init__(self, readings : List[Reading]) -> None:
        self.readings = readings

    def __str__(self) -> str:
        return '\n'.join([str(reading) for reading in self.readings])

    def extrapolate(self) -> List[np.int64]:
        return [reading.extrapolate() for reading in self.readings]
    
    def extrapolate_left(self) -> List[np.int64]:
        return [reading.extrapolate_left() for reading in self.readings]

    @staticmethod
    def from_file(filename) -> 'ReadingList':
        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'r') as file:
            lines = file.readlines()

        return ReadingList([Reading.parse(line) for line in lines])