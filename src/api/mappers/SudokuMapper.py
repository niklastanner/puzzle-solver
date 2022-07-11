import numpy as np

from puzzle_solver.models.grid_games import Sudoku


class SudokuMapper:

    @staticmethod
    def from_json(data):
        raw = data.get('sudoku')
        if type(raw) != np.ndarray:
            raw = np.array(raw)

        if len(raw.shape) == 1:
            sudoku = Sudoku.from_flat_array(raw)
        elif len(raw.shape) == 2:
            sudoku = Sudoku(raw)
        else:
            raise ValueError('Unknown format used to transmit sudoku. Expected 1D or 2D like array.')

        return sudoku
