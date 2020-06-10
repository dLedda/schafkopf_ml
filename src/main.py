from HumanDecisionInterface import HumanDecisionInterface
from SequentialConsoleRenderer import SequentialConsoleRenderer
from Game import Game
from Player import Player
from typing import List


def main() -> None:
    players: List[Player] = get_players()
    renderer = SequentialConsoleRenderer()
    game: Game = Game(players, renderer)
    game.play()


def get_players() -> List[Player]:
    return get_default_players()


def get_default_players() -> List[Player]:
    names = ["Andy", "Ben", "Chris", "Daniel"]
    return list(map(make_new_human_player, names))


def make_new_human_player(name: str) -> Player:
    return Player(name, HumanDecisionInterface(), True)


def get_input_players() -> List[Player]:
    print("Who's playing?")
    p1 = make_new_human_player(input("Player 1: "))
    p2 = make_new_human_player(input("Player 2: "))
    p3 = make_new_human_player(input("Player 3: "))
    p4 = make_new_human_player(input("Player 4: "))
    return [p1, p2, p3, p4]


if __name__ == "__main__":
    main()
