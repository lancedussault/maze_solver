from cell import Cell
import random
import time

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        window=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window = window
        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                cell = Cell(self._window)
                column.append(cell)
            self._cells.append(column)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        

    def _draw_cell(self, i, j):
        if self._window is None:
            return 
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._window is None:
            return
        self._window.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r (self, i, j):
        self._cells[i][j].visited = True

        while True:
            next_index_list = []
            
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return 
        
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited (self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r (self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True
        end_cell = self._cells[self._num_cols - 1][self._num_rows - 1]

        if current == end_cell: 
            return True
        
        possible_directions = []

        if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_left_wall:
            move_right = (i - 1, j)
            possible_directions.append(move_right)
        if i < self._num_cols - 1 and not self._cells[i + 1][j].visited and not self._cells[i][j].has_right_wall:
            move_left = (i + 1, j)
            possible_directions.append(move_left)
        if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j].has_bottom_wall:
            move_down = (i, j - 1)
            possible_directions.append(move_down)
        if j < self._num_rows - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j].has_top_wall:
            move_up = (i, j + 1)
            possible_directions.append(move_up)

        for move in possible_directions:
            Cell.draw_move(self._cells[i][j], self._cells[move[0]][move[1]])
            if self._solve_r(move[0], move[1]):
                return True
            else:
                Cell.draw_move(self._cells[move[0]][move[1]], self._cells[i][j], undo=True)
        
