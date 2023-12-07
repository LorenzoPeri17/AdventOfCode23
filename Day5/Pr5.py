import re, os
import numpy as np
from typing import List, Dict
from dataclasses import dataclass
from tqdm import tqdm
import sys
sys.setrecursionlimit(10000)

# This problem broke me :)

@dataclass
class Range:

    def __init__(self, start : np.int64, range : np.int64):
        self.start : np.int64 = start
        self.range : np.int64 = range
        self.end   : np.int64 = start + range - 1

    def __contains__(self, key : np.int64) -> bool:
        return key >= self.start and key <= self.end
    
    def __str__(self) -> str:
        return f'Range:[{self.start}, {self.end}]'
    
    def __repr__(self) -> str:
        return f'Range:[{self.start}, {self.end}]'
    
    @staticmethod
    def from_to(start: np.int64, end : np.int64) -> 'Range':
        return Range(start, end - start + 1)
    
class RangeList:
    
        def __init__(self, ranges : List[Range]):
            assert isinstance(ranges, list), f'RangeList must be initialized with a list, not {type(ranges)}'
            assert all([isinstance(r, Range) for r in ranges]), f'All elements of RangeList must be of type Range, not {type(ranges[0])}'
            self.ranges = ranges
    
        def __add__(self, other) -> 'RangeList':
            if isinstance(other, Range):
                return RangeList(self.ranges + [other])
            elif isinstance(other, RangeList):
                return RangeList(self.ranges + other.ranges)
            else:
                raise TypeError(f'Cannot add RangeList and {type(other)}')
        
        def __getitem__(self, key : np.int64) -> np.int64:
            self.ranges[key]
        
        def __iter__(self):
            return iter(self.ranges)

        def __len__(self):
            return len(self.ranges)
        
        def min(self):
            return min([r.start for r in self.ranges])
        
        def __str__(self) -> str:
            return f'RangeList: {self.ranges}'
        
        def __repr__(self) -> str:
            return f'RangeList: {self.ranges}'
        
class RangeDictionary:

    def __init__(self, sources : List[np.int64], destinations : List[np.int64], ranges : List[np.int64]):
        self.ranges = ranges
        self.destinations = destinations
        self.sources = sources

        self.range_list = RangeList([Range(s, r) for s, r in zip(sources, ranges)]) 
        self.source_to_dest = {s : d for s, d in zip(sources, destinations)}

    def __getitem__(self, key : np.int64) -> np.int64:
        for s, d, r in zip(self.sources, self.destinations, self.ranges):
            if key >= s and key < s + r:
                return d + (key - s)
        else:
            return key
    
    def on_range(self, range_key : Range) -> RangeList:
        key_start = range_key.start
        key_end = range_key.end
        for dict_range in self.range_list:
            if key_start in dict_range:
                dest = self.source_to_dest[dict_range.start]
                if key_end in dict_range:
                    return RangeList([Range(dest + (key_start - dict_range.start), range_key.range)])
                else:
                    return RangeList([Range.from_to(dest + (key_start - dict_range.start), dest + dict_range.range - 1)]) + self.on_range(Range.from_to(dict_range.end + 1, key_end))
        else:
            # the start is in none of the ranges
            for dict_range in self.range_list:
                if key_end in dict_range:
                    dest = self.source_to_dest[dict_range.start]
                    return self.on_range(Range.from_to(key_start, dict_range.start - 1)) + RangeList([Range(dest, key_end - dict_range.start)])
            else:
                ## we may have to split the range in the middle
                for dict_range in self.range_list:
                    if key_start < dict_range.start and key_end > dict_range.end:
                        dest = self.source_to_dest[dict_range.start]
                        return self.on_range(Range.from_to(key_start, dict_range.start - 1)) + RangeList([Range(dest, dict_range.range)]) + self.on_range(Range.from_to(dict_range.end + 1, key_end))
                else:
                    return RangeList([range_key])


class Mapping:

    def __init__(self, form : str, to : str, map : RangeDictionary ):
        self.form = form
        self.to = to
        self.map = map

class Almanac:

    _seed_pattern = re.compile(r'seeds:([ \d]+)')
    _digit_pattern = re.compile(r'(\d+)')
    _mapping_pattern = re.compile(r'(\w+)-to-(\w+) map:\n([\d \n]+)')
    _SourceStart_DestStart_range_pattern = re.compile(r'(\d+) (\d+) (\d+)')
    _from_to_pattern = re.compile(r'(\w+)-to-(\w+) map:')

    def __init__(self, seeds : np.ndarray[np.int64], mappings : List[Mapping], seed_ranges : RangeList ):
        self.seeds = seeds
        self.mappings = mappings
        self.seed_ranges = seed_ranges

    def _parse_seeds(line : str) -> List[int]:
        m = Almanac._digit_pattern.findall(line)
        return np.array([np.int64(s) for s in m])
    
    def _parse_seeds_P2(line : str) -> List[int]:
        m = Almanac._digit_pattern.findall(line)    
        _seeds_string = [np.int64(s) for s in m]
        seed_start = _seeds_string[0::2]
        seed_ranges = _seeds_string[1::2]
        seeds = np.empty(sum(seed_ranges), dtype=np.int64)

        start_ind = 0
        for start, r in zip(seed_start, seed_ranges, strict=True):
            seeds[start_ind:start_ind+r] = start + np.arange(r)
            start_ind +=r
        return seeds, RangeList([Range(s, r) for s, r in zip(seed_start, seed_ranges)])


    def _parse_mapping(source, dest, map_ranges) -> Mapping:

        # print(f'Parsing mapping from {source} to {dest}')

        source_starts = []
        dest_starts = []
        ranges = []

        for m in Almanac._SourceStart_DestStart_range_pattern.finditer(map_ranges):
            # print(m[0])
            source_starts.append(np.int64(m[2]))
            dest_starts.append(np.int64(m[1]))
            ranges.append(np.int64(m[3]))
        
        mapping = RangeDictionary(source_starts, dest_starts, ranges)

        return Mapping(source, dest, mapping)

    @staticmethod
    def from_file(filename, seeds_are_ranges = False) -> 'Almanac':
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'r') as f:
            lines = ''.join(f.readlines())

        mappings = []

        if seeds_are_ranges:
            seeds, seed_ranges = Almanac._parse_seeds_P2(Almanac._seed_pattern.findall(lines)[0].strip())
        else:
            seeds = Almanac._parse_seeds(Almanac._seed_pattern.findall(lines)[0].strip())
            seed_ranges = RangeList([Range(s, 1) for s in seeds])

        for m in Almanac._mapping_pattern.finditer(lines):
            mapping = Almanac._parse_mapping(m.group(1), m.group(2), m.group(3))
            mappings.append(mapping)

        ordered_mappings = []
        start = 'seed'
        end = 'location'
        while start != end:
            for i, m in enumerate(mappings):
                if m.form == start:
                    ordered_mappings.append(mappings[i])
                    start = m.to
                    break
            else:
                raise ValueError(f'No mapping found for {start}')

        return Almanac(seeds, ordered_mappings, seed_ranges)
    
    def walk(self, value: np.int64, source: str, dest: str) ->  np.int64:

        current_value = value
        current_state = source

        while current_state != dest:
            for m in self.mappings:
                if m.form == current_state:
                    current_value =  m.map[current_value]
                    current_state = m.to
                    break
            else:
                raise ValueError(f'No mapping found for {current_state}')

        return current_value
    
    def walk_seed_loc(self, value: np.int64) ->  np.int64:
        current = value
        for m in self.mappings:
            current =  m.map[current]
        return current
    
    def walk_seed_loc_ranges(self) -> RangeList:
        current = self.seed_ranges
        for m in (self.mappings):
            new = RangeList([])
            for r in current:
                new += m.map.on_range(r)
            current = new
        return new