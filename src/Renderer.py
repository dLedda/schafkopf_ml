from __future__ import annotations
TYPECHECKING = False
if TYPECHECKING:
    from Player import Player
    from Game import TrickState


class Renderer:
    def __init__(self):
        pass

    def render_stack(self, cards: TrickState):
        pass

    def render_hand(self, player: Player):
        pass

    def render_message(self, message: str):
        pass
