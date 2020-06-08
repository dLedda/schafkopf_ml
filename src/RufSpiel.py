from Card import Card
from Player import Player, Player.Id
from typing import List
from Round import Round


class RufSpiel(Round):
    def __init__(self, players: List[Player], spieler_id: Player.Id, spieler):
        super().__init__(players)
        self.variable_trump: Card.Suit = Card.Suit.Herz
        self.spieler: Player.Id =