from puzzle_solver.models.grid_games import GridGame

SUPPORTED_GAME_SIZE = 81
SUPPORTED_CELL_SIZE = 3


class Sudoku(GridGame):
    _cell_size = SUPPORTED_CELL_SIZE

    @staticmethod
    def from_flat_array(array: []):
        game = GridGame.from_flat_array(array)
        if game.get_size() != SUPPORTED_GAME_SIZE:
            raise ValueError('Only board sizes of 9x9 are supported.')

    def get_cell_size(self):
        return self._cell_size

    def print(self):
        cell_size = self._cell_size
        size = self.get_height()
        for i, row in enumerate(self.game):
            print(("|" + " {} {} {} |" * cell_size).format(*[x if x != 0 else " " for x in row]))
            if i != 0 and i % cell_size == 2 and not i == size - 1:
                print("|" + "+".join(["-------"] * cell_size) + "|")
