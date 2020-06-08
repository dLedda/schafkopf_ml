from Card import Card
from typing import List


class Deck(list):
    def __init__(self):
        deck = []
        for rank in Card.Rank:
            for suit in Card.Suit:
                deck.append(Card(suit, rank))
        super().__init__(deck)
