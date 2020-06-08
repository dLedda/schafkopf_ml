from typing import Dict, List
from Card import Card
from collections import namedtuple


SUIT_COLOR: Dict[Card.Suit, str] = {
    Card.Suit.Eichel: "Black",
    Card.Suit.Gras: "Green",
    Card.Suit.Herz: "Red",
    Card.Suit.Schellen: "Yellow",
}
CARD_GLYPH_CHARS: List[str] = [
    "R     S",
    "       ",
    "   S   ",
    "       ",
    "S     R",
]
CARD_GLYPH_COLOR: List[str] = [
    "QWWWWWS",
    "WWWWWWW",
    "WWWSWWW",
    "WWWWWWW",
    "SWWWWWQ",
]
C_COLOR: Dict[str, str] = {
    "Green": "\033[32;107m",
    "Red": "\033[31;107m",
    "Yellow": "\033[33;107m",
    "Black": "\033[30;107m",
    "ResetAll": "\033[0m",
    "TextReset": "\033[0m",
    "BgReset": "\033[1;30m",
}
Glyph = namedtuple("Glyph", "chars colors")
C_COLOR_FROM_GLYPH_CHAR: Dict[str, str] = {
    "Q": C_COLOR["Black"],
    "R": C_COLOR["Red"],
    "G": C_COLOR["Green"],
    "Y": C_COLOR["Yellow"],
    "D": C_COLOR["ResetAll"],
    "W": C_COLOR["Black"],
}
GLYPH_CHAR: Dict[str, str] = {
    "Black": "Q",
    "Red": "R",
    "Green": "G",
    "Yellow": "Y",
    "Default": "D",
    "WhiteBg": "W",
}


def glyph_for(card: Card) -> Glyph:
    glyph = Glyph(CARD_GLYPH_CHARS.copy(), CARD_GLYPH_COLOR.copy())
    for i, line in enumerate(glyph.chars):
        glyph.chars[i] = line.replace("S", Card.SUITS_STR[card.suit]).replace("R", Card.RANKS_STR[card.rank])
    for i, line in enumerate(glyph.colors):
        glyph.colors[i] = line.replace("S", GLYPH_CHAR[SUIT_COLOR[card.suit]])
    return glyph


def glyph_to_colored_string(glyph):
    out = ""
    for chars_line, colors_line in zip(glyph.chars, glyph.colors):
        for char, color_code in zip(chars_line, colors_line):
            out += C_COLOR_FROM_GLYPH_CHAR[color_code] + char + C_COLOR["ResetAll"]
        out += "\n"
    return out


def side_by_side_glyphs(cards: List[Card]) -> Glyph:
    glyph = Glyph([""] * len(CARD_GLYPH_CHARS), [""] * len(CARD_GLYPH_CHARS))
    for card in cards:
        for i, glyph_char_line in enumerate(glyph_for(card).chars):
            glyph.chars[i] += glyph_char_line + " "
        for i, glyph_color_line in enumerate(glyph_for(card).colors):
            glyph.colors[i] += glyph_color_line + GLYPH_CHAR["Default"]
    return glyph


def stacked_glyphs(cards: List[Card]):
    result_width = len(CARD_GLYPH_CHARS[0]) + len(cards) - 1
    result_height = len(CARD_GLYPH_CHARS) + len(cards) - 1
    result = Glyph([" " * result_width] * result_height, [GLYPH_CHAR["Default"] * result_width] * result_height)
    for i, card in enumerate(reversed(cards)):
        origin_coord = [i, i]
        for j, (chars_line, glyph_colors_line) in enumerate(zip(glyph_for(card).chars, glyph_for(card).colors)):
            chars_out = result.chars[j + origin_coord[0]]
            colors_out = result.colors[j + origin_coord[0]]
            chars_out = chars_out[:origin_coord[1]] + chars_line
            colors_out = colors_out[:origin_coord[1]] + glyph_colors_line
            result.chars[j + origin_coord[0]] = chars_out
            result.colors[j + origin_coord[0]] = colors_out
    return result