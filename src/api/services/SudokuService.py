import logging
from time import time

from puzzle_solver.scanners import SudokuScanner
from puzzle_solver.solver import SudokuSolver

log = logging.getLogger(__name__)


class SudokuService:

    def __init__(self):
        self._scanner = SudokuScanner()
        self._solver = SudokuSolver()

    def solve_sudoku(self, image):
        log.debug('Scan Sudoku')
        start = time()
        sudoku = self._scanner.scan(image)
        end = time()
        log.debug(f'Took {round(end - start, 2)}s to analyze the Image')

        log.debug('Solve Sudoku')
        start = time()
        solutions = self._solver.solve(sudoku)
        end = time()
        log.debug(f'Took {round(end - start, 2)}s to solve the Sudoku')

        return solutions
