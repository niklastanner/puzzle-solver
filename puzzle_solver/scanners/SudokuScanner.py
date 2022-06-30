import logging

import cv2
import numpy as np
import pytesseract

from tqdm import tqdm

from puzzle_solver.models.grid_games import Sudoku
from puzzle_solver.scanners import GridGameScanner

PATH_TO_TESSERACT_EXECUTABLE = r'E:\Program Files\Tesseract-OCR\tesseract.exe'
log = logging.getLogger(__name__)


class SudokuScanner(GridGameScanner):

    @staticmethod
    def convert_to_binary_image(image):
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thr = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 23)
        return thr

    @staticmethod
    def find_numbers_in_tiled_image(image, tiles):
        cells = []
        for tile in tqdm(tiles):
            cutout = np.copy(image[tile['row_start']:tile['row_end'], tile['col_start']:tile['col_end']])
            cutout = SudokuScanner.add_border_to_image(cutout, 10)

            # psm=10: Treat the image as single character
            # -c tessedit_char_whitelist=123456789: Limit the searched characters to 123456789
            cell = pytesseract.image_to_string(cutout, config='--psm 10 -c tessedit_char_whitelist=123456789')
            if cell:
                try:
                    cell = int(cell)
                except ValueError:
                    print(f'Unable to parse {cell} to int!')
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
        pytesseract.pytesseract.tesseract_cmd = PATH_TO_TESSERACT_EXECUTABLE
        cells = self.find_numbers_in_tiled_image(binary, tiles)

        log.debug('Convert to sudoku model')
        sudoku = Sudoku.from_flat_array(cells)

        return sudoku
