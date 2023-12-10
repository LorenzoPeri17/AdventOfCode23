import re, os
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from tqdm import tqdm
from enum import Enum, unique

###### PART 1 ######

@unique
class Card(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __hash__(self):
        return hash(self.name)
    
    @staticmethod
    def str_to_card(s : str) -> 'Card':
        if s == 'A':
            return Card.ACE
        elif s == 'K':
            return Card.KING
        elif s == 'Q':
            return Card.QUEEN
        elif s == 'J':
            return Card.JACK
        elif s == 'T':
            return Card.TEN
        else:
            return Card(int(s) - 2)
        
    @staticmethod
    def card_to_str(c : 'Card') -> str:
        if c == Card.ACE:
            return 'A'
        elif c == Card.KING:
            return 'K'
        elif c == Card.QUEEN:
            return 'Q'
        elif c == Card.JACK:
            return 'J'
        elif c == Card.TEN:
            return 'T'
        else:
            return str(c.value + 2)
    
    @staticmethod
    def parse(s : str) -> 'Card':
        return Card.str_to_card(s)

class Point(Enum):

    FIVE_A_KIND = 6
    FOUR_A_KIND = 5
    FULL_HOUSE  = 4
    THREE_A_KIND = 3
    TWO_PAIRS   = 2
    ONE_PAIR    = 1
    HIGH_CARD   = 0

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __eq__(self, other):
        return self.value == other.value

class Hand:

    _hand_pattern = re.compile(r'([2-9AKQTJ]{5}) +(\d+)')

    def __init__(self, hand : List[Card], bid : Card) -> None:

        self.hand : List[Card] = hand
        self.bid : int = bid

        unique, counts = np.unique(hand, return_counts=True)
        self.counts = dict(zip(unique, counts))

        self.rank : int | None = None

        self.points : Point = self._get_points()

    def __str__(self) -> str:
        return f'Hand: {self.hand}, Bid: {self.bid}'
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        if self.points == other.points:
            for i in range(5):
                if self.hand[i] != other.hand[i]:
                    return self.hand[i] < other.hand[i]
            else:
                raise ValueError('Comparing two identical hands')
        else:
            return self.points < other.points
        
    def __gt__(self, other):
        if self.points == other.points:
            for i in range(5):
                if self.hand[i] != other.hand[i]:
                    return self.hand[i] > other.hand[i]
            else:
                raise ValueError('Comparing two identical hands')
        else:
            return self.points > other.points
    
    def _get_points(self) -> Point:
        if max(self.counts.values()) == 5:
            return Point.FIVE_A_KIND
        elif max(self.counts.values()) == 4:
            return Point.FOUR_A_KIND
        elif max(self.counts.values()) == 3 and min(self.counts.values()) == 2:
            return Point.FULL_HOUSE
        elif max(self.counts.values()) == 3:
            return Point.THREE_A_KIND
        elif max(self.counts.values()) == 2 and len(self.counts) == 3:
            return Point.TWO_PAIRS
        elif max(self.counts.values()) == 2:
            return Point.ONE_PAIR
        else:
            return Point.HIGH_CARD
        
    def hand_str(self) -> str:
        return ''.join([Card.card_to_str(c) for c in self.hand])
        
    @staticmethod
    def parse(s : str) -> 'Hand':
        
        hand, bid = Hand._hand_pattern.search(s).groups()
        bid = int(bid)
        hand = [Card.parse(c) for c in hand]
        
        return Hand(hand, bid)
    
###### PART 2 ######
@unique
class Card_P2(Enum):
    JOKER = -1
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    QUEEN = 10
    KING = 11
    ACE = 12

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __hash__(self):
        return hash(self.name)
    
    @staticmethod
    def str_to_card(s : str) -> 'Card_P2':
        if s == 'A':
            return Card_P2.ACE
        elif s == 'K':
            return Card_P2.KING
        elif s == 'Q':
            return Card_P2.QUEEN
        elif s == 'J':
            return Card_P2.JOKER
        elif s == 'T':
            return Card_P2.TEN
        else:
            return Card_P2(int(s) - 2)
        
    @staticmethod
    def card_to_str(c : 'Card_P2') -> str:
        if c == Card_P2.ACE:
            return 'A'
        elif c == Card_P2.KING:
            return 'K'
        elif c == Card_P2.QUEEN:
            return 'Q'
        elif c == Card_P2.JOKER:
            return 'J'
        elif c == Card_P2.TEN:
            return 'T'
        else:
            return str(c.value + 2)
    
    @staticmethod
    def parse(s : str) -> 'Card_P2':
        return Card_P2.str_to_card(s)
    
class Hand_P2:

    _hand_pattern = re.compile(r'([2-9AKQTJ]{5}) +(\d+)')

    def __init__(self, hand : List[Card_P2], bid : Card) -> None:

        self.hand : List[Card_P2] = hand
        self.bid : int = bid

        unique, counts = np.unique(hand, return_counts=True)
        self.counts = dict(zip(unique, counts))

        self.rank : int | None = None

        self.points : Point = self._get_points()

    def __str__(self) -> str:
        return f'Hand: {self.hand}, Bid: {self.bid}'
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        if self.points == other.points:
            for i in range(5):
                assert isinstance(self.hand[i], Card_P2)
                assert isinstance(other.hand[i], Card_P2)
                if self.hand[i] != other.hand[i]:
                    return self.hand[i] < other.hand[i]
            else:
                raise ValueError('Comparing two identical hands')
        else:
            return self.points < other.points
        
    def __gt__(self, other):
        if self.points == other.points:
            for i in range(5):
                if self.hand[i] != other.hand[i]:
                    return self.hand[i] > other.hand[i]
            else:
                raise ValueError('Comparing two identical hands')
        else:
            return self.points > other.points
    
    def _get_points(self) -> Point:
        if Card_P2.JOKER not in self.counts.keys():
            if max(self.counts.values()) == 5:
                return Point.FIVE_A_KIND
            elif max(self.counts.values()) == 4:
                return Point.FOUR_A_KIND
            elif max(self.counts.values()) == 3 and min(self.counts.values()) == 2:
                return Point.FULL_HOUSE
            elif max(self.counts.values()) == 3:
                return Point.THREE_A_KIND
            elif max(self.counts.values()) == 2 and len(self.counts) == 3:
                return Point.TWO_PAIRS
            elif max(self.counts.values()) == 2:
                return Point.ONE_PAIR
            else:
                return Point.HIGH_CARD
        else:

            _count_no_joker = self.counts.copy()
            del _count_no_joker[Card_P2.JOKER]
            number_of_jokers = self.counts[Card_P2.JOKER]

            assert number_of_jokers > 0
            assert number_of_jokers <= 5

            if number_of_jokers == 5:                   # 5 Jokers
                return Point.FIVE_A_KIND
            

            elif max(_count_no_joker.values()) == 4:    # 1 poker, 1 Joker
                assert number_of_jokers == 1
                assert len(_count_no_joker) == 1
                return Point.FIVE_A_KIND
            

            elif max(_count_no_joker.values()) == 3:
                if number_of_jokers == 1:               # 1 triple, 1 single, 1 Joker
                    assert len(_count_no_joker) == 2
                    assert list(sorted(_count_no_joker.values())) == [1, 3]
                    return Point.FOUR_A_KIND
                else:                                   # 1 triple, 2 Jokers
                    assert number_of_jokers == 2
                    assert len(_count_no_joker) == 1
                    return Point.FIVE_A_KIND
                

            elif max(_count_no_joker.values()) == 2:
                if number_of_jokers == 3:               # 1 pair, 3 Jokers
                    assert len(_count_no_joker) == 1
                    return Point.FIVE_A_KIND
                elif number_of_jokers == 2:             # 1 pair, 1 single, 2 Jokers
                    assert len(_count_no_joker) == 2
                    assert list(sorted(_count_no_joker.values())) == [1, 2]
                    return Point.FOUR_A_KIND
                else: # only 1 Joker
                    assert number_of_jokers == 1
                    if len(_count_no_joker) == 2:       # 2 pairs, 1 Joker
                        assert list(sorted(_count_no_joker.values())) == [2, 2]
                        return Point.FULL_HOUSE
                    else:                               # 1 pair, 2 singles, 1 Joker
                        assert len(_count_no_joker) == 3
                        assert list(sorted(_count_no_joker.values())) == [1, 1, 2]
                        return Point.THREE_A_KIND
                    

            elif max(_count_no_joker.values()) == 1:
                if number_of_jokers == 4:               # 1 single, 4 Jokers
                    assert len(_count_no_joker) == 1
                    return Point.FIVE_A_KIND
                elif number_of_jokers == 3:             # 2 singles, 3 Jokers
                    assert len(_count_no_joker) == 2
                    assert list(sorted(_count_no_joker.values())) == [1, 1]
                    return Point.FOUR_A_KIND
                elif number_of_jokers == 2:             # 3 singles, 2 Jokers
                    assert len(_count_no_joker) == 3
                    assert list(sorted(_count_no_joker.values())) == [1, 1, 1]
                    return Point.THREE_A_KIND
                else:                                   # 4 singles, 1 Joker
                    assert number_of_jokers == 1
                    assert len(_count_no_joker) == 4
                    assert list(sorted(_count_no_joker.values())) == [1, 1, 1, 1]
                    return Point.ONE_PAIR
                

            else:                                       # Something went wrong
                raise ValueError(f'Invalid hand: {self.hand}')
            
    def hand_str(self) -> str:
        return ''.join([Card_P2.card_to_str(c) for c in self.hand])
        
    @staticmethod
    def parse(s : str) -> 'Hand_P2':
        
        hand, bid = Hand_P2._hand_pattern.search(s).groups()
        bid = int(bid)
        hand = [Card_P2.parse(c) for c in hand]
        
        return Hand_P2(hand, bid)
    
## HANDLIST ##

class HandList:

    def __init__(self, hands : List[Hand] | List[Hand_P2], sort : bool = True) -> None:
        self.hands = hands
        if sort:
            self._sort()
        else:
            self.sorted = False

    def __str__(self) -> str:
        return str(self.hands)
    
    def __repr__(self):
        return str(self)
    
    def __getitem__(self, i):
        return self.hands[i]
    
    def __len__(self):
        return len(self.hands)
    
    def _sort(self):
        self.hands.sort(reverse = False)
        self.sorted = True
        for i in range(len(self.hands)):
            self.hands[i].rank = i + 1
    
    def get_total(self) -> int:
        if not self.sorted:
            self._sort()
        return sum([h.bid * h.rank for h in self.hands])
    
    @staticmethod
    def from_file(filename : str, sort : bool = True, P2 : bool = False) -> 'HandList':
        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        if P2:
            hands = [Hand_P2.parse(l) for l in lines]
        else:
            hands = [Hand.parse(l) for l in lines]

        return HandList(hands, sort = sort)