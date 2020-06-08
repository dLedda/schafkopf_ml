from typing import List
from Player import Player
from Game import Game
from ConsoleRenderer import ConsoleRenderer


def main() -> None:
    players: List[Player] = get_players()
    renderer = ConsoleRenderer()
    game: Game = Game(players, renderer)
    game.play()


def get_players():
    return get_default_players()


def get_default_players() -> List[Player]:
    names = ["Andy", "Ben", "Chris", "Daniel"]
    return list(map(Player, names))


def get_input_players() -> List[Player]:
    print("Who's playing?")
    p1 = Player(input("Player 1: "))
    p2 = Player(input("Player 2: "))
    p3 = Player(input("Player 3: "))
    p4 = Player(input("Player 4: "))
    return [p1, p2, p3, p4]


if __name__ == "__main__":
    main()
