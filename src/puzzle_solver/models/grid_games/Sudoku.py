import cv2
import numpy as np

from puzzle_solver.models.grid_games import GridGame

SUPPORTED_GAME_SIZE = 81
SUPPORTED_CELL_SIZE = 3


class Sudoku(GridGame):
    _cell_size = SUPPORTED_CELL_SIZE

    @staticmethod
    def from_flat_array(array: []):
        game = super(Sudoku, Sudoku).from_flat_array(array)
        if game.get_size() != SUPPORTED_GAME_SIZE:
            raise ValueError('Only board sizes of 9x9 are supported.')
        return Sudoku(game.game)

    def get_cell_size(self):
        return self._cell_size

    def _get_optimal_font_scale(self, text, width, height):
        for scale in range(60, 0, -1):
            textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale / 10, thickness=1)
            new_width = textSize[0][0]
            new_height = textSize[0][1]
            if new_width <= width and new_height <= height:
                return scale / 10
        return 1

    def to_image(self, width=500, height=500, colored=True):
        image = np.full((height, width, 3), 255, np.float)
        x_step = width // 9
        y_step = height // 9
        font_scale = self._get_optimal_font_scale('0', x_step - 20, y_step - (height // 25))

        # Draw board
        x = x_step
        y = y_step
        for i in range(len(self.game) - 1):
            cv2.line(image, (0, y + (y_step // 5)), (width, y + (y_step // 5)), (0, 0, 0), 2)
            cv2.line(image, (x, 0), (x, height), (0, 0, 0), 2)
            x += x_step
            y += y_step

        # Draw numbers
        initial_game = self.initial_game()
        y = height // 9
        for i, row in enumerate(self.game):
            x = x_step // 5
            for j, value in enumerate(row):
                if value != 0:
                    if initial_game[i][j] != 0:
                        color = (0, 0, 0)  # Black numbers if they were given
                    else:
                        color = (0, 0, 255)  # Colored numbers if they were found by solver

                    text = str(value)
                    cv2.putText(image,
                                text,
                                (x, y),
                                cv2.FONT_HERSHEY_DUPLEX,
                                font_scale,
                                color,
                                2)
                x += x_step
            y += y_step

        return image

    def to_string(self):
        s = ''
        cell_size = self._cell_size
        size = self.get_height()
        for i, row in enumerate(self.game):
            s += ("|" + " {} {} {} |" * cell_size).format(*[x if x != 0 else " " for x in row]) + '\n'
            if i != 0 and i % cell_size == 2 and not i == size - 1:
                s += "|" + "+".join(["-------"] * cell_size) + "|" + '\n'
        return s

    def print(self):
        print(self.to_string())
