import configparser
import logging as log
from time import time

import cv2

from puzzle_solver.scanners import SudokuScanner
from puzzle_solver.solver import SudokuSolver


def load_image(path_to_image):
    img = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Not necessary, since grayscale RGB equals grayscale BGR
    assert img is not None, f'Error opening image {path_to_image}'
    return img


log.basicConfig()
log.getLogger().setLevel(log.DEBUG)

if __name__ == '__main__':
    sudoku1 = [
        [1, 0, 0, 0, 3, 0, 0, 8, 0],
        [0, 6, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 9, 3, 0, 0],
        [0, 4, 5, 0, 0, 6, 0, 0, 7],
        [9, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 8, 0, 0, 3, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 9, 5, 6],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 8, 0, 1, 0]
    ]
    sudoku2 = [
        [4, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 3, 2],
        [0, 0, 6, 0, 0, 8, 2, 5, 0],
        [0, 9, 0, 0, 0, 0, 0, 8, 0],
        [0, 3, 7, 6, 0, 0, 9, 0, 0],
        [2, 7, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 4]
    ]
    sudoku3 = [
        [8, 0, 0, 3, 0, 2, 0, 0, 7],
        [0, 4, 0, 0, 6, 0, 0, 9, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 0],
        [1, 0, 0, 6, 0, 8, 0, 0, 5],
        [0, 3, 0, 0, 2, 0, 0, 1, 0],
        [4, 0, 0, 7, 0, 3, 0, 0, 6],
        [0, 0, 6, 0, 0, 0, 8, 0, 0],
        [0, 2, 0, 0, 3, 0, 0, 6, 0],
        [5, 0, 0, 2, 0, 6, 0, 0, 1]
    ]
    sudoku4 = [
        [0, 0, 6, 1, 0, 0, 0, 0, 8],
        [0, 7, 0, 0, 9, 0, 0, 2, 0],
        [3, 0, 0, 0, 0, 6, 9, 0, 0],
        [6, 0, 0, 0, 0, 2, 3, 0, 0],
        [0, 8, 0, 0, 4, 0, 0, 1, 0],
        [0, 0, 4, 3, 0, 0, 0, 0, 9],
        [0, 0, 9, 2, 0, 0, 0, 0, 4],
        [0, 5, 0, 0, 7, 0, 0, 8, 0],
        [8, 0, 0, 0, 0, 5, 1, 0, 0]
    ]

    # sudoku = Sudoku(sudoku1)

    img1 = '../../PoC/img/sudoku-800x800.png'
    img2 = '../../PoC/img/sudoku-481x512.jpeg'

    scanner = SudokuScanner()

    log.debug('Load image')
    image = load_image(img1)
    log.debug('Scan image')
    start = time()
    sudoku = scanner.scan(image)
    end = time()
    log.debug(f'Took {round(end - start, 2)}s to analyze the Image')

    log.debug('Solve Sudoku')
    solver = SudokuSolver()
    start = time()
    solution = solver.solve(sudoku)
    end = time()
    log.debug(f'Took {round(end - start, 2)}s to solve the Sudoku')
    solution.print()
