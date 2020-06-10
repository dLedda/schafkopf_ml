from __future__ import annotations
from typing import List, Union, NamedTuple
from Card import Card
from copy import deepcopy
from Game import Move, RoundType
from enum import Enum
TYPECHECKING = False
if TYPECHECKING:
    from DecisionMaker import DecisionMaker
    from Game import TrickState


Hand = List[Card]
Trick = List[Card]


class GameChoice(NamedTuple):
    type: Union[RoundType, None]
    suit: Union[Card.Suit, None]
    tout: bool


class Player:
    Id = int
    instances = 0

    @classmethod
    def get_new_id(cls):
        new_id = cls.instances
        cls.instances += 1
        return new_id

    def __init__(self, name: str, decision_maker: DecisionMaker, is_human: bool):
        self.id = self.get_new_id()
        self.human_controlled: bool = is_human
        self.name: str = name
        self.hand: Hand = []
        self.tricks: List[Trick] = []
        self.decision_maker: DecisionMaker = decision_maker

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

    def get_tricks(self) -> List[Trick]:
        return deepcopy(self.tricks)

    def get_name(self):
        return self.name

    def get_id(self) -> int:
        return self.id

    def make_decision(self, trick_state: TrickState) -> Move:
        return Move(
            self.play_card(self.decision_maker.make_decision(trick_state, self.hand)),
            self.get_id()
        )

    def choose_round_type(self, sauspiel_choices: List[Card.Suit]) -> None:
        self.decision_maker.choose_round_type(self.hand, sauspiel_choices)

    def game_choice(self) -> Union[RoundType, None]:
        return self.game_choice()

    def calc_score_for_tricks(self) -> int:
        return sum([int(card) for trick in self.tricks for card in trick])

    def is_human(self):
        return self.human_controlled

