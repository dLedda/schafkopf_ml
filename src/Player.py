from typing import List, Tuple
from Card import Card
from copy import deepcopy


Hand = List[Card]
Trick = Tuple[Card, Card, Card, Card]


class Player:
    Id = int
    instances = 0

    @classmethod
    def get_new_id(cls):
        new_id = cls.instances
        cls.instances += 1
        return new_id

    def __init__(self, name: str):
        self.id = self.get_new_id()
        self.name: str = name
        self.hand: Hand = []
        self.tricks: List[Trick] = []

    def __str__(self):
        return self.name

    def deal_cards(self, *cards: List[Card]) -> None:
        self.hand += cards

    def card_options(self) -> List[Card]:
        return self.hand.copy()

    def add_trick(self, trick: Trick) -> None:
        self.tricks.append(trick)

    def play_card(self, card_index) -> Card:
        return self.hand.pop(card_index)

    def reset(self) -> None:
        self.tricks = []
        self.hand = []

    def tricks(self) -> List[Trick]:
        return deepcopy(self.tricks)

    def get_name(self):
        return self.name

    def get_id(self) -> int:
        return self.id