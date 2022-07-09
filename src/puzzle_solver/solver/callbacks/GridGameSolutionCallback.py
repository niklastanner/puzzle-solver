from ortools.sat.python import cp_model

from puzzle_solver.models.grid_games import GridGame


class GridGameSolutionCallback(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    _solutions = set()

    def __init__(self, variables, game_type=GridGame, limit=None):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables
        self._solution_count = 0
        self._game_type = game_type
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1

        width = len(self._variables[0])
        height = len(self._variables)
        solution = []
        for i in range(height):
            for j in range(width):
                solution.append(self.Value(self._variables[i][j]))
        self._solutions.add(self._game_type.from_flat_array(solution))

        if self._solution_limit is not None and self._solution_count >= self._solution_limit:
            print('Stop search after %i solutions' % self._solution_limit)
            self.StopSearch()

    def solutions(self):
        return self._solutions

    def solution_count(self):
        return self._solution_count
