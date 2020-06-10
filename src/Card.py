import enum
from typing import *
from Errors import SchafkopfError


class Card:
    class OpError(SchafkopfError, TypeError):
        def __init__(self):
            self.message = "An '{}' object may only be operated on with others of the same type.".format(
                Card.__class__.__name__)

    class Suit(enum.Enum):
        Eichel = 3
        Gras = 2
        Herz = 1
        Schellen = 0

    class Rank(enum.Enum):
        Ass = 7
        Koenig = 6
        Ober = 5
        Unter = 4
        Zehn = 3
        Neun = 2
        Acht = 1
        Sieben = 0

    RANK_SCORE: Dict[Rank, int] = {
        Rank.Ass: 11,
        Rank.Koenig: 4,
        Rank.Ober: 3,
        Rank.Unter: 2,
        Rank.Zehn: 10,
        Rank.Neun: 0,
        Rank.Acht: 0,
        Rank.Sieben: 0,
    }

    def __init__(self, suit: Suit, rank: Rank):
        self.suit: Card.Suit = suit
        self.rank: Card.Rank = rank

    def __str__(self):
        return self.suit.name + " " + self.rank.name

    def __repr__(self):
        return "Card: <" + self.suit.name + ", " + self.rank.name + ">"

    def __gt__(self, other):
        if type(other) != Card:
            raise Card.OpError()
        else:
            return self.suit.value > other.suit.value or self.rank.value > other.rank.value

    def __lt__(self, other):
        if type(other) != Card:
            raise Card.OpError()
        else:
            return self.suit.value < other.suit.value or self.rank.value < other.rank.value

    def __add__(self, other):
        if type(other) != Card:
            raise Card.OpError()
        else:
            return Card.RANK_SCORE[self.rank] + Card.RANK_SCORE[other.rank]

    def __sub__(self, other):
        if type(other) != Card:
            raise Card.OpError()
        else:
            return Card.RANK_SCORE[self.rank] - Card.RANK_SCORE[other.rank]

    def __int__(self):
        return Card.RANK_SCORE[self.rank]

    def rep(self) -> Tuple[Suit, Rank]:
        return self.suit, self.rank
