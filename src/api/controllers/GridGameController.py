import logging

from flask import request, Blueprint, send_file

from api.mappers import ImageMapper
from api.services import SudokuService

log = logging.getLogger(__name__)
grid_game_controller = Blueprint('api_controller', __name__, template_folder='templates')
sudoku_service = SudokuService()


@grid_game_controller.route('/', methods=['POST'])
def solve_grid_game():
    return "<p>This method is meant to detect and solve any grid game.<br>It is not yet implemented.</p>"


@grid_game_controller.route('/sudoku', methods=['POST'])
def solve_sudoku():
    log.info('Received Sudoku to solve')
    file = request.files['image']
    image = ImageMapper.from_api(file)
    solution = sudoku_service.solve_sudoku(image)
    log.info('Finished solving Sudoku')
    img_io = ImageMapper.from_image(solution.to_image())
    return send_file(img_io,
                     attachment_filename='solved_sudoku.png',
                     mimetype='image/png')
