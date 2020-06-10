from __future__ import annotations
import random as rn
from itertools import cycle
from enum import Enum
from typing import List, Union, NamedTuple, Dict, Tuple
from Errors import GameLevelError
from Card import Card
from Deck import Deck

TYPECHECKING = False
if TYPECHECKING:
    from Player import Player, Hand, GameChoice
    from Renderer import Renderer


class RoundType(Enum):
    Sauspiel = "Sauspiel"
    Wenz = "Wenz"
    Farbsolo = "Farbsolo"
    Ramsch = "Ramsch"


class Round(NamedTuple):
    type: RoundType
    isFarbSolo: bool
    trumpSuit: Union[Card.Suit, None]


class Turn(NamedTuple):
    suit: Card.Suit
    isTrumpTurn: bool


class Move(NamedTuple):
    card: Card
    playerId: Player.Id


Trick = List[Card]
TrickState = List[Move]
CardRep = Tuple[Card.Suit, Card.Rank]
CardRanking = Dict[CardRep, int]


class Game:
    PLAYER_COUNT = 4
    TRICK_SIZE = PLAYER_COUNT

    SAUSPIEL_TRUMP_ORDER: List[CardRep] = [
        (Card.Suit.Eichel, Card.Rank.Ober),
        (Card.Suit.Gras, Card.Rank.Ober),
        (Card.Suit.Herz, Card.Rank.Ober),
        (Card.Suit.Schellen, Card.Rank.Ober),
        (Card.Suit.Eichel, Card.Rank.Unter),
        (Card.Suit.Gras, Card.Rank.Unter),
        (Card.Suit.Herz, Card.Rank.Unter),
        (Card.Suit.Schellen, Card.Rank.Unter),
    ]

    def __init__(self, players: List[Player], renderer: Renderer):
        if len(players) != Game.PLAYER_COUNT:
            raise GameLevelError("There must be exactly four players, but received " + str(len(players)) + "!")

        self.renderer: Renderer = renderer

        self.players: List[Player] = players
        self.current_player_index: int = 0
        self.last_trick_winner_index: int = 0
        self.dealer_index: int = 0

        self.game_over: bool = False
        self.round_over: bool = False
        self.round_count: int = 0
        self.trick_count: int = 0
        self.round_details: Round = Round(
            type=RoundType.Sauspiel,
            isFarbSolo=False,
            trumpSuit=Card.Suit.Herz
        )
        self.round_trump_ranking: CardRanking = {}
        self.trick_details: Turn = Turn(
            suit=Card.Suit.Schellen,
            isTrumpTurn=False
        )

        self.deck = Deck()
        self.current_trick: TrickState = []

    def play(self) -> None:
        self.renderer.render_message("Game start!")
        while not self.game_over:
            self.round_count += 1
            self.trick_count = 0
            self.current_player_index = self.neighbour_index(self.dealer_index, after=True)
            self.play_round()
            self.dealer_index = self.neighbour_index(self.dealer_index, after=True)
        self.renderer.render_message("Game end!")

    def play_round(self) -> None:
        self.renderer.render_message("Round {} start!".format(self.round_count))
        self.deal_cards()
        self.determine_game_type()
        self.update_trump_ranking()
        for i in range(len(self.deck) // Game.PLAYER_COUNT):
            self.trick_count += 1
            self.current_trick.clear()
            self.play_trick()
            self.current_player_index = self.last_trick_winner_index
        self.renderer.render_message("Round Results:")
        for player in self.players:
            score = player.calc_score_for_tricks()
            self.renderer.render_message("{}: {} points.".format(player.get_name(), score))
        self.renderer.render_message("Round end!")

    def determine_game_type(self) -> None:
        player_choosing = self.current_player_index
        player = None
        for i in range(len(self.players)):
            self.renderer.render_hand(self.players[player_choosing])
            sauspiel_choices = self.sauspiel_choices_for_hand(self.players[player_choosing].card_options())
            self.players[player_choosing].choose_round_type(sauspiel_choices)
            player_choosing = self.neighbour_index(player_choosing, after=True)

    def sauspiel_choices_for_hand(self, hand: Hand) -> List[Card.Suit]:
        has_card = {
            Card.Suit.Eichel: {"ass": False, "normal": False},
            Card.Suit.Gras: {"ass": False, "normal": False},
            Card.Suit.Schellen: {"ass": False, "normal": False}
        }
        choices: List[Card.Suit] = []
        for card in hand:
            if card.suit != Card.Suit.Herz:
                if card.rank not in [Card.Rank.Ober, Card.Rank.Unter, Card.Rank.Ass]:
                    has_card[card.suit]["normal"] = True
                elif card.rank == Card.Rank.Ass:
                    has_card[card.suit]["ass"] = True
        for suit in has_card:
            if has_card[suit]["normal"] and not has_card[suit]["ass"]:
                choices.append(suit)
        return choices

    def update_trump_ranking(self) -> None:
        rank_val = 0
        if self.round_details.type == RoundType.Sauspiel:
            for card_type in Game.SAUSPIEL_TRUMP_ORDER:
                self.round_trump_ranking[card_type] = rank_val
                rank_val += 1
            for rank in Card.Rank:
                if rank != Card.Rank.Ober and rank != Card.Rank.Unter:
                    self.round_trump_ranking[(self.round_details.trumpSuit, rank)] = rank_val
                rank_val += 1

    def play_trick(self) -> None:
        self.renderer.render_message("Turn {} start.".format(self.trick_count))
        for i in range(len(self.players)):
            self.renderer.render_hand(self.current_player())
            self.make_move_for_current_player()
            self.renderer.render_stack(self.current_trick)
            self.proceed_to_next_player()
        winning_move: Move = self.determine_winning_move(self.current_trick)
        self.last_trick_winner_index = winning_move.playerId
        winner = self.players[self.last_trick_winner_index]
        winner.add_trick([move.card for move in self.current_trick])
        self.renderer.render_message("{p} won the trick with the card: {c}".format(
            p=winner.get_name(), c=winning_move.card))
        self.renderer.render_message("Turn end.")

    def deal_cards(self) -> None:
        rn.shuffle(self.deck)
        player_iterator = cycle(self.players)
        for i in range(0, len(self.deck), 4):
            dealt_cards = self.deck[i:i + 4]
            next(player_iterator).deal_cards(*dealt_cards)

    def make_move_for_current_player(self) -> None:
        self.current_trick.append(
            self.current_player().make_decision(self.current_trick.copy())
        )
        if self.last_trick_winner_index == self.current_player_index:
            self.trick_details = Turn(
                suit=self.current_trick[0].card.suit,
                isTrumpTurn=self.current_trick[0].card.suit == self.round_details.trumpSuit)

    def round_is_over(self) -> bool:
        return self.round_over

    def proceed_to_next_player(self) -> None:
        self.current_player_index = self.neighbour_index(self.current_player_index, after=True)

    def neighbour_index(self, player_index: int, after: bool = True) -> int:
        neighbour = player_index + 1 if after else player_index - 1
        if neighbour >= len(self.players):
            neighbour = 0
        elif neighbour < 0:
            neighbour = len(self.players) - 1
        return neighbour

    def set_starting_player(self) -> None:
        self.current_player_index = rn.randint(0, len(self.players) - 1)

    def determine_winning_move(self, trick: TrickState) -> Move:
        best_move = trick[0]
        for move in trick:
            if self.round_details.type == RoundType.Sauspiel:
                if move.card.rep() in self.round_trump_ranking:
                    if best_move.card.rep() in self.round_trump_ranking:
                        if self.new_move_wins_trump_trick(best_move, move):
                            best_move = move
                    else:
                        best_move = move
                elif move.card.suit == self.trick_details.suit and move.card > best_move.card:
                    best_move = move
        return best_move

    def new_move_wins_trump_trick(self, old_move: Move, new_move: Move) -> bool:
        return self.round_trump_ranking[new_move.card.rep()] < self.round_trump_ranking[old_move.card.rep()]

    def trick_value(self, trick: TrickState) -> int:
        return sum([move.card for move in trick])

    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def current_dealer(self) -> Player:
        return self.players[self.dealer_index]
