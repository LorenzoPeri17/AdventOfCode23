import re, os
import numpy as np
from typing import List, Dict, Tuple, Union
from dataclasses import dataclass
from tqdm import tqdm

def DummyGenerator():
  while True:
    yield

@dataclass(slots=True)
class Node:
    
    name  : str
    left  : Union['Node', None]
    right : Union['Node', None]

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
    
class UroborosIterator:
    
        def __init__(self, iterable):
            self.iterable = iterable
            self.len_minus_one = len(iterable) - 1
            self.index = 0
        
        def __next__(self):
            result = self.iterable[self.index]

            if self.index == self.len_minus_one:
                self.index = 0
            else:
                self.index += 1

            return result

class UroborosString:

    __slots__ = ("string", "len")

    def __init__(self, string : str):
        self.string = string
        self.len = len(string)
    
    def __getitem__(self, key):
        return self.string[key%self.len]
    
    def __iter__(self) -> UroborosIterator:
        return UroborosIterator(self.string)

    def __len__(self):
        return len(self.string)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string
    
class NodeGraph:

    _node_pattern  = re.compile(r'([1-9A-Z]{3}) = \(([1-9A-Z]{3}), ([1-9A-Z]{3})\)')
    _directions_pattern = re.compile(r'([RL]+)')

    def __init__(self, directions : str):

        self.directions = directions

        self.nodes : Dict[str, Node] = {}

        self.root  : Union['Node', None] = None
        self.end   : Union['Node', None] = None

    def __str__(self):
        return f'NodeGraph({self.directions}), {self.nodes.values()}'
    
    def add_node(self, name : str, left : str, right : str):

        if left not in self.nodes:
            self.nodes[left] = Node(left, None, None)

        if right not in self.nodes:
            self.nodes[right] = Node(right, None, None)

        if name not in self.nodes:
            self.nodes[name] = Node(name, self.nodes[left], self.nodes[right])
        else:
            self.nodes[name].left  = self.nodes[left]
            self.nodes[name].right = self.nodes[right]

        if name == 'AAA':
            self.root = self.nodes[name]
        elif name == 'ZZZ':
            self.end  = self.nodes[name]
    
    def parse_node(self, line : str):

        groups = self._node_pattern.findall(line)

        if not groups:
            raise ValueError(f'Could not parse line: {line}')
        
        name, left, right = groups[0]

        self.add_node(name, left, right)

    @staticmethod
    def from_file(filename : str) -> 'NodeGraph':

        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'r') as f:
            directions_line = f.readline().strip()
            directions = NodeGraph._directions_pattern.findall(directions_line)[0]

            f.readline() # Skip empty line

            graph = NodeGraph(directions)

            lines = f.readlines()

        for line in lines:
            graph.parse_node(line)

        return graph

    def walk_path(self) -> int:

        steps = 0
        current_node = self.root

        direction_counter = 0

        while current_node != self.end:

            direction = self.directions[direction_counter%len(self.directions)]

            if direction == 'L':
                current_node = current_node.left
            elif direction == 'R':
                current_node = current_node.right
            else:
                raise ValueError(f'Invalid direction: {direction}')

            steps += 1
            direction_counter += 1

        return steps

    def walk_simultaneous_paths(self) -> int:

        current_nodes = [node for node in self.nodes.values() if node.name.endswith('A')]
        
        steps = 0

        _len_dir = len(self.directions)

        for _ in tqdm(DummyGenerator()): # Infinite loop keeping track of performance

            direction = self.directions[steps%_len_dir]

            if direction == 'L':
                current_nodes = [node.left for node in current_nodes]
            else: # direction == 'R':
                current_nodes = [node.right for node in current_nodes]

            steps += 1

            for node in current_nodes:
                if node.name[-1] != 'Z':
                    break
            else:
                break
        
        print()
        return steps
    
    def walk_simultaneous_paths_hardstop(self, hardstop : int = 10_000_000) -> int:

        current_nodes = [node for node in self.nodes.values() if node.name.endswith('A')]
        # current_nodes = np.array([node for node in self.nodes.values() if node.name.endswith('A')])
        
        steps = 0

        _len_dir = len(self.directions)
        _keep_going = True

        # for _ in tqdm(DummyGenerator()): # Infinite loop keeping track of performance
        # while _keep_going:
        while True:

            if steps%100_000 == 0:
                print(f'{steps}', end = '\r')

            direction = self.directions[steps%_len_dir]

            if direction == 'L':
                current_nodes = [node.left for node in current_nodes]
                # for i, node in enumerate(current_nodes):
                #     new_node = node.left
                #     current_nodes[i] = new_node
                #     if new_node.name[-1] != 'Z':
                #         _keep_going = True
            else: # direction == 'R':
                current_nodes = [node.right for node in current_nodes]
                # for i, node in enumerate(current_nodes):
                #     new_node = node.right
                #     current_nodes[i] = new_node
                #     if new_node.name[-1] != 'Z':
                #         _keep_going = True

            steps += 1

            # if all((node.name[-1] == 'Z' for node in current_nodes)):
            #     break

            for node in current_nodes:
                if node.name[-1] != 'Z':
                    break
            else:
                break

            if steps >= hardstop:
                break
        
        print()
        return steps

    def walk_simultaneous_paths_iter(self) -> int:

        current_nodes = [node for node in self.nodes.values() if node.name.endswith('A')]

        for steps, direction in tqdm(enumerate(UroborosString(self.directions), start = 1)): 
            # Infinite loop keeping track of performance

            if direction == 'L':
                current_nodes = [node.left for node in current_nodes]
            else: # direction == 'R':
                current_nodes = [node.right for node in current_nodes]

            # if all((node.name[-1] == 'Z' for node in current_nodes)):
            #     break

            for node in current_nodes:
                if node.name[-1] != 'Z':
                    break
            else:
                break

        print()
        return steps

    def walk_simultaneous_paths_lmc(self) -> int:

        start_nodes = [node for node in self.nodes.values() if node.name.endswith('A')]
        
        steps = 0

        _len_dir = len(self.directions)
        periods = []

        for current_node in start_nodes:

            steps = 0
            while True:

                direction = self.directions[steps%_len_dir]

                if direction == 'L':
                    current_node = current_node.left
                else: # direction == 'R':
                    current_node = current_node.right

                steps += 1
                
                if current_node.name[-1] == 'Z':
                        break
            
            periods.append(steps)

        steps = np.lcm.reduce(periods)
        
        return steps