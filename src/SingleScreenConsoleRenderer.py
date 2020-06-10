from Renderer import Renderer
from typing import List
from Player import Player
from Card import Card
from Glyph import side_by_side_glyphs, stacked_glyphs, glyph_to_colored_string
from Game import TrickState
import os


class SingleScreenConsoleRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.header = ""
        self.stack = ""
        self.hand = ""

    def render_stack(self, trick_state: TrickState):
        self.stack = glyph_to_colored_string(stacked_glyphs([move.card for move in trick_state]))
        self.rerender()

    def render_hand(self, player: Player):
        self.hand = player.get_name() + "'s hand:\n" + \
                    glyph_to_colored_string(side_by_side_glyphs(player.card_options()))
        self.rerender()

    def render_message(self, message: str):
        self.header = message
        self.rerender()

    def rerender(self):
        os.system("clear")
        print(self.header)
        print()
        print("Current Stack: ")
        print(self.stack)
        print(self.hand)