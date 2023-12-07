import re, os
import numpy as np
from typing import List

from dataclasses import dataclass

class Card:

    _card_pattern = re.compile(r'^Card +([\d]+)')
    _number_pattern = re.compile(r'([\d]+)')

    def __init__(self, card_number, winning_numbers, numbers):
        self.card_number     : int          = card_number
        self.winning_numbers : List[int]    = winning_numbers
        self.numbers         : List[int]    = numbers

        self.found           : int          
        self.points          : int          
        self.copies          : int          = 1

        self.get_points()

    def get_points(self):
        found = 0
        for number in self.numbers:
            if number in self.winning_numbers:
                found += 1
        self.found = found
        points =  pow(2, found-1) if found > 0 else 0
        self.points = points
        return points

    @staticmethod
    def from_line(line) -> 'Card':

        number_string, card_string = line.split(':')
        card_number = int(Card._card_pattern.search(number_string).group(1))

        winning, had = card_string.split('|')

        winning_numbers = [int(m.group(1)) for m in Card._number_pattern.finditer(winning)]

        numbers = [int(m.group(1)) for m in Card._number_pattern.finditer(had)]

        return Card(card_number, winning_numbers, numbers)

def Cards_from_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r') as f:
        lines = f.readlines()
        cards = []
        for line in lines:
            cards.append(Card.from_line(line))
        return cards

def generate_copies(cards : List[Card]) -> List[Card]:
    for i, card in enumerate(cards):
        for j in range(card.found):

            ind = i + j + 1

            if ind >= len(cards):
                break

            cards[ind].copies += card.copies