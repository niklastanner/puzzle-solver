import numpy as np


class Game:
    _initial_game = None
    game = None

    def __init__(self, game: np.ndarray):
        self._initial_game = game.copy()
        self.game = game

    def initial_game(self) -> np.ndarray:
        return self._initial_game
