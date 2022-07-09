import configparser
import logging
import os
from itertools import product

from ortools.sat.python import cp_model

from puzzle_solver.models.grid_games import Sudoku
from puzzle_solver.solver import Solver
from puzzle_solver.solver.callbacks import GridGameSolutionCallback

log = logging.getLogger(__name__)


class SudokuSolver(Solver):
    game = None
    _solutions = set()

    def __init__(self):
        super().__init__()
        self._config = configparser.ConfigParser()
        self._config.read(os.environ.get('PUZZLE_SOLVER_CONFIG_FILE'))

    def stringify(self, game: Sudoku):
        arr = []
        for row in game.game:
            r = []
            for value in row:
                if value == 0:
                    r.append('')
                else:
                    try:
                        r.append(str(value))
                    except ValueError:
                        raise ValueError(f'Only numbers between 0-9 allowed. Got {value} instead')
            arr.append(r)
        return arr

    def configure_board(self, model):
        cell_size = self.game.get_cell_size()
        board_size = cell_size * cell_size
        board_indices = list(product(range(board_size), repeat=2))  # tuples (i, j) for all board indices
        cell_indices = list(product(range(cell_size), repeat=2))  # tuples (i, j) for all cell indices
        board = [
            [model.NewIntVar(1, board_size, f"({_i},{_j})") for _j in range(board_size)]
            for _i in range(board_size)
        ]

        return board_indices, cell_indices, board

    def add_constraints(self, model, board, board_indices, cell_indices, game):
        game_representation = self.stringify(game)

        # Assign existing numbers
        for i, j in board_indices:
            if len(game_representation[i][j]) > 0:  # elements are strings, so check for length
                model.Add(board[i][j] == int(game_representation[i][j]))  # and cast back to int

        # All lines and columns have to be different
        board_size = game.get_height()
        for i in range(board_size):
            model.AddAllDifferent([board[i][j] for j in range(board_size)])  # rows
            model.AddAllDifferent([board[j][i] for j in range(board_size)])  # columns

        # All 3x3 sub-matrix contains only different values
        cell_size = game.get_cell_size()
        for i, j in cell_indices:
            model.AddAllDifferent(
                [board[i * cell_size + di][j * cell_size + dj] for di in range(cell_size) for dj in range(cell_size)]
            )

    def solve(self, game):
        self.game = game
        model = cp_model.CpModel()
        board_indices, cell_indices, board = self.configure_board(model)
        self.add_constraints(model, board, board_indices, cell_indices, self.game)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self._config['solver'].getfloat('time_limit')
        solver.parameters.enumerate_all_solutions = True
        solution_callback = GridGameSolutionCallback(board, Sudoku)
        status = solver.Solve(model, solution_callback)

        log.debug(f'Solver status = {solver.StatusName(status)}')
        log.debug(f'Number of solutions found: {solution_callback.solution_count()}')

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            self._solutions = solution_callback.solutions()
            return self._solutions
        else:
            log.error('Unable to solve Sudoku')
            return None

    def get_solutions(self):
        return self._solutions
