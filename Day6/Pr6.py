import re, os
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from tqdm import tqdm

@dataclass
class Race:
    duration         : int
    distance_to_beat : int

    def __str__(self) -> str:
        return f'Race: {self.duration} ms, Record:{self.distance_to_beat} mm'
    
    def __repr__(self):
        return str(self)
    
    def find_hold(self) -> Tuple[float, float]:
        _det = np.sqrt(self.duration**2 - 4*self.distance_to_beat)
        return 0.5 * (self.duration + _det), 0.5 * (self.duration - _det)
    
    def get_winning_numbers(self) -> np.int32:
        maxhold, minhold = self.find_hold()
        return np.int32(np.floor(maxhold) - np.ceil(minhold)) + 1 - 2*(np.floor(maxhold) == maxhold)

    @staticmethod
    def from_file_no_spaces(filename) -> 'Race':
        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'r') as f:
            lines = ''.join(f.readlines())
        
        time = int(Races._time_pattern.search(lines)[1].replace('\t', '').replace(' ', ''))
        dist = int(Races._dist_pattern.search(lines)[1].replace('\t', '').replace(' ', ''))

        return Race(time, dist)

class Races:

    _digit_pattern = re.compile(r'(\d+)')
    _time_pattern  = re.compile(r'Time:[ \t]*([\d \t]+)')
    _dist_pattern  = re.compile(r'Distance:[ \t]*([\d \t]+)')

    def __init__(self, races : List[Race]) -> None:
        self.races = races

    def __str__(self):
        return str(self.races)
    
    def __repr__(self):
        return str(self)

    @staticmethod
    def from_file(filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'r') as f:
            lines = ''.join(f.readlines())
        
        times = [int(t) for t in Races._digit_pattern.findall(Races._time_pattern.search(lines)[1])]
        dists = [int(t) for t in Races._digit_pattern.findall(Races._dist_pattern.search(lines)[1])]

        races = [Race(t, d) for t, d in zip(times, dists)]

        return Races(races)
    
    def get_winning_numbers(self) -> List[np.int32]:
        return [r.get_winning_numbers() for r in self.races]


