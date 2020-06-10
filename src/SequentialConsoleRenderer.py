from Renderer import Renderer
from typing import List
from Player import Player
from Card import Card
from Glyph import side_by_side_glyphs, stacked_glyphs, glyph_to_colored_string
from Game import TrickState
import os


class SequentialConsoleRenderer(Renderer):
    def __init__(self):
        super().__init__()

    def render_stack(self, trick_state: TrickState):
        print(glyph_to_colored_string(stacked_glyphs([move.card for move in trick_state])))

    def render_hand(self, player: Player):
        print(player.get_name() + "'s hand:\n" + glyph_to_colored_string(side_by_side_glyphs(player.card_options())))

    def render_message(self, message: str):
        print(message)
