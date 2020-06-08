import enum
from typing import *
from collections import namedtuple


class Card:
    class Suit(enum.Enum):
        Eichel = 0
        Gras = 1
        Herz = 2
        Schellen = 3

    SUITS_STR: Dict[Suit, str] = {
        Suit.Eichel: "♣",
        Suit.Gras: "♠",
        Suit.Herz: "♥",
        Suit.Schellen: "♦",
    }

    class Rank(enum.Enum):
        Ober = 0
        Unter = 1
        Ass = 2
        Koenig = 3
        Zehn = 4
        Neun = 5
        Acht = 6
        Sieben = 7

    RANKS_STR: Dict[Rank, str] = {
        Rank.Ober: "O",
        Rank.Unter: "U",
        Rank.Ass: "A",
        Rank.Koenig: "K",
        Rank.Zehn: "X",
        Rank.Neun: "9",
        Rank.Acht: "8",
        Rank.Sieben: "7",
    }

    def __init__(self, suit: Suit, rank: Rank):
        self.suit: Card.Suit = suit
        self.rank: Card.Rank = rank

    def __str__(self):
        return "\n".join(self.glyph())

    def __repr__(self):
        return "Card: <" + self.suit.name + ", " + self.rank.name + ">"




