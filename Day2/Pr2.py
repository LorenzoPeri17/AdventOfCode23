import re, os
from dataclasses import dataclass
from typing import List

@dataclass
class Round:
    red : int       = 0
    green : int     = 0
    blue : int      = 0

class Game:

    _game_pattern = re.compile(r'^Game ([\d]+)')
    _round_pattern = re.compile(r'([\d]+) (blue|red|green)')

    def __init__(self, number:int, *rounds : List[Round]) -> None:
        self.number : int           = number
        self.rounds : List[Round]   = rounds

    def get_total_reds(self) -> int:
        return max(round.red for round in self.rounds)
    
    def get_total_greens(self) -> int:
        return max(round.green for round in self.rounds)
    
    def get_total_blues(self) -> int:
        return max(round.blue for round in self.rounds)
    
    def is_possible(self) -> bool:
        return  self.get_total_reds() <= 12 and \
                self.get_total_greens() <= 13 and \
                self.get_total_blues() <= 14
    
    def get_power(self):
        return self.get_total_reds() * self.get_total_greens() * self.get_total_blues()
    
    @staticmethod
    def from_line(line) -> 'Game':
        number_string, round_string = line.split(':')
        number = int(Game._game_pattern.search(number_string).group(1))
        rounds = []
        for round in round_string.split(';'):
            round = round.strip()

            if round == '':
                raise ValueError('Empty round')
            
            colors = [color.strip() for color in round.split(',')]

            if len(colors) > 3:
                raise ValueError('Invalid round')
            
            round_dict = {}
            for color in colors:
                if not (match := Game._round_pattern.match(color)):
                    raise ValueError('Invalid round') 
                round_dict[match.group(2)] = int(match.group(1))

            rounds.append(Round(**round_dict))
                
        return Game(number, *rounds)

def get_Games_from_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    games = []
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            games.append(Game.from_line(line))
    return games


