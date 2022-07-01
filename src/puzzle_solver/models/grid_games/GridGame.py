import math

import numpy as np

from src.puzzle_solver.models import Game


class GridGame(Game):

    @staticmethod
    def from_flat_array(array: []):
        if GridGame.is_square(array):
            size = int(math.sqrt(len(array)))
            return GridGame(np.reshape(array, (size, size)))
        else:
            raise ValueError('Size of array needs to be quadratic!')

    @staticmethod
    def is_square(array: []) -> bool:
        return len(array) == math.isqrt(len(array)) ** 2

    def get_height(self) -> int:
        return len(self.game)

    def get_size(self) -> int:
        return len(self.flatten())

    def flatten(self) -> []:
        return self.game.flatten()
