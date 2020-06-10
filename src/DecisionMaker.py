from __future__ import annotations
from Game import RoundType
from typing import Union, List
TYPECHECKING = False
if TYPECHECKING:
    from Player import Hand, GameChoice
    from Card import Card
    from Game import TrickState


class DecisionMaker:
    def __init__(self):
        pass

    def make_decision(self, trick_state: TrickState, hand: Hand) -> int:
        raise NotImplementedError("This is an abstract base class!")

    def choose_round_type(self, hand: Hand, sauspiel_choices: List[Card.Suit]) -> GameChoice:
        raise NotImplementedError("This is an abstract base class!")
