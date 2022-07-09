import argparse
import configparser
import logging as log
import os
import sys
from time import time

import cv2
from matplotlib import pyplot as plt
from pytesseract import pytesseract

from puzzle_solver.scanners import SudokuScanner
from puzzle_solver.solver import SudokuSolver

CONFIG_DEV_FILE = '../resources/config-dev.ini'


def configure_logger(level=log.INFO):
    log.basicConfig()
    log.getLogger().setLevel(level)


def load_command_line_arguments():
    log.debug('Number of arguments:', len(sys.argv), 'arguments.')
    log.debug('Argument List:', str(sys.argv))

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action="store_true", help="run in dev mode")
    parser.add_argument("-p", "--prod", action="store_true", help="run in prod mode")
    args = parser.parse_args()

    if args.dev and args.prod:
        log.warning('Cannot run dev and prod mode simultaneously. Running dev mode instead.')
        args.dev = True
        args.prod = False

    if not args.dev and not args.prod:
        args.dev = True

    return args


def load_environment(args):
    if args.dev:
        config_file = CONFIG_DEV_FILE
    else:
        raise EnvironmentError('This file is designed to run in dev mode. But is being started in prod mode instead.')

    os.environ['PUZZLE_SOLVER_CONFIG_FILE'] = config_file
    assert os.path.exists(config_file), f'{config_file} does not exist'
    config = configparser.ConfigParser()
    config.read(config_file)
    log.debug(config.items())
    assert 'general' in config, 'Config file does not exist or is not properly configured'
    return config


def load_image(path_to_image):
    img = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Not necessary, since grayscale RGB equals grayscale BGR
    assert img is not None, f'Error opening image {path_to_image}'
    return img


if __name__ == '__main__':
    args = load_command_line_arguments()
    config = load_environment(args)
    debug = False
    log_level = config['general'].getint('log_level')
    if log_level == log.DEBUG:
        debug = True

    configure_logger(log_level)

    pytesseract.tesseract_cmd = config['tesseract']['executable']  # needed if not running inside docker

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
    solutions = solver.solve(sudoku)
    end = time()
    log.debug(f'Took {round(end - start, 2)}s to solve the Sudoku')
    for solution in solutions:
        plt.imshow(solution.to_image())
        solution.print()
    plt.show()
