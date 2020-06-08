from Player import Player
from typing import List
from Round import Round
from RufSpiel import RufSpiel
from Card import Card
from Deck import Deck
from Renderer import Renderer
from Errors import GameLevelError
import random as rn
from itertools import cycle


Stack = List[Card]


class Game:
    def __init__(self, players: List[Player], renderer: Renderer):
        if len(players) != 4:
            raise GameLevelError("There must be exactly four players, but received " + str(len(players)) + "!")
        self.players: List[Player] = players
        self.game_over: bool = False
        self.renderer = renderer
        self.deck = Deck()
        self.stack: List[Card] = []
        self.current_round: Round = RufSpiel(self.players)

    def play(self):
        self.renderer.render_message("Game start!")
        while not self.game_over:
            self.current_round = Round(self.players)
            self.play_round()
            self.game_over = True
        self.renderer.render_message("Game end!")

    def play_round(self):
        self.deal_cards()
        while not self.current_round.is_over():
            self.stack.clear()
            self.round_turn()
            self.renderer.render()
            self.current_round.next_turn()

    def round_turn(self):
        self.renderer.render_message("Turn {} start.".format(self.current_round.turns_taken() + 1))
        for i in range(len(self.players)):
            self.renderer.render_hand(self.current_player())
            self.make_move_for_current_player()
            self.renderer.render_stack(self.stack)
            if self.current_round.turn_in_progress():
                self.current_round.move_turn_to_next_player()
        self.renderer.render_message("Turn end.")

    def deal_cards(self) -> None:
        rn.shuffle(self.deck)
        player_iterator = cycle(self.players)
        for i in range(0, len(self.deck), 4):
            dealt_cards = self.deck[i:i + 4]
            next(player_iterator).deal_cards(*dealt_cards)

    def current_player(self):
        return self.players[self.current_round.get_current_player_index()]

    def make_move_for_current_player(self) -> None:
        cards_to_choose_from: List[Card] = self.current_player().card_options()
        card_index_choice = None
        while card_index_choice is None:
            try:
                attempt = int(input("Choose a card -> "))
                if len(cards_to_choose_from) >= attempt > 0:
                    card_index_choice = attempt - 1
                else:
                    print("Choice was outside card range.")
            except ValueError:
                print("Invalid choice.")
        self.stack.append(self.current_player().play_card(card_index_choice))

    def last_cards_played(self, num_cards: int) -> Stack:
        if len(self.stack) == 0:
            return []
        elif len(self.stack) == 1:
            return [self.stack[0]]
        else:
            if num_cards > len(self.stack):
                num_cards = len(self.stack)
            return self.stack[-num_cards:]

    def get_stack(self) -> Stack:
        return self.stack.copy()
