from Player import Player
from Errors import RoundLevelError
from typing import List
import random as rn


class Round:
    def __init__(self, players: List[Player]):
        self.current_player_index: int = 0
        self.round_ended: bool = False
        self.turn_number: int = 1
        self.moves_left_in_turn: int = len(players)
        self.num_players = len(players)

    def gen_player_list(self, players: List[Player]):
        return list(map(lambda x: x.get_id(), players))

    def turns_taken(self) -> int:
        return self.turn_number - 1

    def turn_in_progress(self) -> bool:
        return self.moves_left_in_turn > 0

    def is_over(self) -> bool:
        return self.round_ended or self.turn_number > 8

    def next_turn(self) -> None:
        self.turn_number += 1
        self.current_player_index = 0

    def move_turn_to_next_player(self) -> None:
        if not self.turn_in_progress():
            raise RoundLevelError("Cannot move to the next player if all players have already made their move!")
        self.current_player_index += 1
        if self.current_player_index >= self.num_players:
            self.current_player_index = 0

    def get_current_player_index(self) -> int:
        return self.current_player_index
