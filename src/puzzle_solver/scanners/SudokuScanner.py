import configparser
import logging
import os

import cv2
import numpy as np
import pytesseract
from tqdm import tqdm

from puzzle_solver.models.grid_games import Sudoku
from puzzle_solver.scanners import GridGameScanner

log = logging.getLogger(__name__)

CHAR_BLACKLIST = ['\n', '\r', '\t', '\f', '\v', '\n\f', '\r\n']


class SudokuScanner(GridGameScanner):

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read(os.environ.get('PUZZLE_SOLVER_CONFIG_FILE'))

    @staticmethod
    def convert_to_binary_image(image):
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thr = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 23)
        return thr

    def find_numbers_in_tiled_image(self, image, tiles):
        cells = []

        log_level = self._config['general'].getint('log_level')
        if log_level == logging.DEBUG:
            iterator = tqdm(tiles)
        else:
            iterator = tiles

        for tile in iterator:
            cutout = np.copy(image[tile['row_start']:tile['row_end'], tile['col_start']:tile['col_end']])
            cutout = SudokuScanner.add_border_to_image(cutout, 10)

            # psm=10: Treat the image as single character
            # -c tessedit_char_whitelist=123456789: Limit the searched characters to 123456789
            cell = pytesseract.image_to_string(cutout, config='--psm 10 -c tessedit_char_whitelist=123456789')
            if cell and cell not in CHAR_BLACKLIST:
                try:
                    cell = int(cell)
                except ValueError:
                    log.warning(f'Unable to parse {repr(cell)} to int!')
                    cell = 0
            else:
                cell = 0

            cells.append(cell)
        return cells

    def scan(self, image):
        preprocessed_image, tiles = super().scan(image)

        log.debug('Convert image to binary image')
        binary = self.convert_to_binary_image(preprocessed_image)
        binary = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)

        log.debug('Scan tiles using OCR')
        cells = self.find_numbers_in_tiled_image(binary, tiles)

        log.debug('Convert to sudoku model')
        sudoku = Sudoku.from_flat_array(cells)

        return sudoku
