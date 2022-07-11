import logging

from flask import request, Blueprint, send_file

from api.mappers import ImageMapper, SudokuMapper
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
    data = request.json
    sudoku = SudokuMapper.from_json(data)
    solutions = sudoku_service.solve_sudoku(sudoku)
    log.info('Finished solving Sudoku')
    zip_io = ImageMapper.from_images([solution.to_image() for solution in solutions])
    return send_file(zip_io,
                     as_attachment=True,
                     attachment_filename='solved_sudoku.zip')


@grid_game_controller.route('/sudoku/image', methods=['POST'])
def solve_sudoku_by_image():
    log.info('Received image of Sudoku to solve')
    file = request.files['image']
    image = ImageMapper.from_api(file)
    solutions = sudoku_service.solve_sudoku_by_image(image)
    log.info('Finished solving Sudoku')
    zip_io = ImageMapper.from_images([solution.to_image() for solution in solutions])
    return send_file(zip_io,
                     as_attachment=True,
                     attachment_filename='solved_sudoku.zip')
