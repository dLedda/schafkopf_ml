from __future__ import annotations
from DecisionMaker import DecisionMaker
from Player import GameChoice
from Game import RoundType
from typing import List
from Card import Card
TYPECHECKING = False
if TYPECHECKING:
    from Player import Hand
    from Game import TrickState


class HumanDecisionInterface(DecisionMaker):
    def __init__(self):
        super().__init__()

    def make_decision(self, trick_state: TrickState, hand: Hand) -> int:
        card_index_choice = None
        while card_index_choice is None:
            try:
                attempt = int(input("Choose a card -> "))
                if len(hand) >= attempt > 0:
                    card_index_choice = attempt - 1
                else:
                    print("Choice was outside card range.")
            except ValueError:
                print("Invalid choice.")
        return card_index_choice

    def choose_round_type(self, hand: Hand, sauspiel_choices: List[Card.Suit]) -> GameChoice:
        type_choice = self.prompt_round_type(sauspiel_choices)
        suit_choice = None
        if type_choice not in [RoundType.Wenz, None]:
            suit_choice = self.prompt_suit(type_choice, sauspiel_choices)
        playing_tout = False
        if type_choice in [RoundType.Wenz, RoundType.Farbsolo]:
            playing_tout = self.prompt_tout()
        return GameChoice(type_choice, suit_choice, playing_tout)

    def prompt_round_type(self, sauspiel_choices: List[Card.Suit]) -> RoundType:
        round_types = [None] + \
                      ([RoundType.Sauspiel] if len(sauspiel_choices) > 0 else []) + \
                      [RoundType.Farbsolo, RoundType.Wenz]
        type_choice = None
        type_was_chosen = False
        while not type_was_chosen:
            try:
                print("Choose a game to play: ")
                print(", ".join(
                    ["Pass (1)"] + ["{} ({})".format(round_type.name, i + 1) for i, round_type in enumerate(round_types)
                                    if round_type is not None]))
                attempt = int(input(" -> "))
                type_choice = round_types[attempt - 1]
                type_was_chosen = True
            except ValueError:
                print("Invalid input.")
            except IndexError:
                print("Invalid choice.")
        return type_choice

    def prompt_suit(self, type_choice: RoundType, sauspiel_choices: List[Card.Suit]) -> Card.Suit:
        suit_choice = None
        while suit_choice is None:
            try:
                suit_types = [suit for suit in Card.Suit] if type_choice != RoundType.Sauspiel else sauspiel_choices
                print("Choose a suit to play with: ")
                print(", ".join(["{} ({})".format(suit.name, i + 1) for i, suit in enumerate(suit_types)]))
                attempt = int(input(" -> "))
                suit_choice = suit_types[attempt - 1]
            except ValueError:
                print("Invalid input.")
            except IndexError:
                print("Invalid choice.")
        return suit_choice

    def prompt_tout(self) -> bool:
        attempt = input("Will you play Tout? (Y/N) -> ")
        return attempt == "Y"
