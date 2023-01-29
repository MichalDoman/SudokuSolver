from tkinter import *

SIDE = 100
MARGIN = 50
WIDTH = 9 * SIDE + 2 * MARGIN
HEIGHT = WIDTH


class SudokuSolver:
    def __init__(self, board_cells, board_squares):
        self.cells = board_cells
        self.squares = board_squares
        self.solve()
    def solve(self):
        while not self.check_if_solved():
            self.check_row()
            self.check_column()
            self.check_square()
        print('Sudoku solved!')

    def check_if_solved(self):
        for row in self.cells:
            for cell in row:
                if not cell.value:
                    return False
        return True

    def check_row(self):
        for cells_in_row in self.cells:
            values = []
            for cell in cells_in_row:
                if cell.value:
                    values.append(cell.value)
            self.update_cells(values, cells_in_row)

    def check_column(self):
        for col_nr in range(0, 9):
            cells_in_column = []
            values = []
            for row in self.cells:
                cell = row[col_nr]
                cells_in_column.append(cell)
                if cell.value:
                    values.append(cell.value)
            self.update_cells(values, cells_in_column)

    def check_square(self):
        for square in self.squares:
            values = []
            for cell in square:
                if cell.value:
                    values.append(cell.value)
            self.update_cells(values, square)

    @staticmethod
    def update_cells(values, influence_cells):
        for cell in influence_cells:
            for value in values:
                if not cell.value:
                    if value in cell.possible_values:
                        cell.possible_values.remove(value)

            if len(cell.possible_values) == 1 and not cell.value:
                value = cell.possible_values[0]
                cell.show_digit(value, 'slate grey')


class Board(Frame):
    def __init__(self, master):
        super().__init__(master)
        # Prepare canvas and buttons:
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=BOTTOM)

        self.reset_button = Button(self, text='Reset', width=24, bd=3, bg='OrangeRed3', fg='white',
                                   activebackground='OrangeRed4', activeforeground='white', font=('Script', 10, 'bold'),
                                   relief="flat", command=self.reset_board)
        self.reset_button.pack(fill=BOTH, expand=True, side=LEFT)

        self.solve_button = Button(self, text='Solve', width=24, bd=3, bg='chartreuse4', fg='white',
                                   activebackground='dark green', activeforeground='white', font=('Script', 10, 'bold'),
                                   relief="flat", command=self.solve)
        self.solve_button.pack(fill=BOTH, expand=True, side=RIGHT)

        # Create cells and organise them:
        self.draw_grid()
        self.cells = []
        self.create_cells()
        self.current_cell = self.cells[4][4]
        self.current_cell.highlight()
        self.squares = []
        self.create_squares(self.cells)

        # Bind necessary keys:
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.choose_cell)
        self.canvas.bind("<Key>", self.choose_digit)
        self.canvas.bind("<Up>", self.switch_cells_with_arrows)
        self.canvas.bind("<Down>", self.switch_cells_with_arrows)
        self.canvas.bind("<Left>", self.switch_cells_with_arrows)
        self.canvas.bind("<Right>", self.switch_cells_with_arrows)
        self.canvas.bind("<space>", lambda key_press: self.delete_digit())
        self.canvas.bind("<BackSpace>", lambda key_press: self.delete_digit())

        self.is_solved = False

    def draw_grid(self):
        for line_nr in range(10):
            # change color and line width for every 3rd line:
            color = 'grey'
            line_width = 1
            if (line_nr + 3) % 3 == 0:
                color = 'black'
                line_width = 3

            # draw vertical lines:
            x = MARGIN + line_nr * SIDE
            y1 = (HEIGHT - MARGIN)
            y2 = MARGIN
            self.canvas.create_line(x, y1, x, y2, fill=color, width=line_width)

            # draw horizontal lines:
            x1 = MARGIN
            x2 = WIDTH - MARGIN
            y = HEIGHT - MARGIN - line_nr * SIDE
            self.canvas.create_line(x1, y, x2, y, fill=color, width=line_width)

    def create_cells(self):
        for row_nr in range(9):
            row = []

            for col_nr in range(9):
                x1 = MARGIN + col_nr * SIDE
                y1 = MARGIN + row_nr * SIDE
                x2 = x1 + SIDE
                y2 = y1 + SIDE
                list_coord = (row_nr, col_nr)  # Used for moving with arrows
                cell = Cell(self.canvas, list_coord, x1, y1, x2, y2)
                row.append(cell)

            self.cells.append(row)

    def create_squares(self, cells):
        for square_x in range(0, 9, 3):  # for 0, 3 and 6
            for square_y in range(0, 9, 3):
                square = []
                for row in range(square_x, square_x + 3):  # (0, 3), (3, 6) and (6, 9)
                    for col in range(square_y, square_y + 3):
                        cell = cells[row][col]
                        square.append(cell)
                self.squares.append(square)

    def choose_cell(self, click_coord):
        x = click_coord.x
        y = click_coord.y

        for row in self.cells:
            for col in range(9):
                cell = row[col]
                if cell.x1 <= x <= cell.x2 and cell.y1 <= y <= cell.y2:
                    cell.highlight()
                    self.current_cell = cell
                    break

    def choose_digit(self, key_press):
        if not self.is_solved:
            if self.current_cell:
                key_char = key_press.char
                if key_char.isdigit() and int(key_char) != 0:
                    self.current_cell.show_digit(int(key_press.char), 'black')

    def delete_digit(self):
        if not self.is_solved:
            self.canvas.delete(self.current_cell.unique_tag)

    def switch_cells_with_arrows(self, arrow_press):
        arrow = arrow_press.keysym

        if arrow == 'Right':
            list_row = self.current_cell.list_coord[0]
            list_col = self.current_cell.list_coord[1] + 1

        elif arrow == 'Left':
            list_row = self.current_cell.list_coord[0]
            list_col = self.current_cell.list_coord[1] - 1

        elif arrow == 'Up':
            list_row = self.current_cell.list_coord[0] - 1
            list_col = self.current_cell.list_coord[1]

        else:
            list_row = self.current_cell.list_coord[0] + 1
            list_col = self.current_cell.list_coord[1]

        if list_row < 0:
            list_row = 8
        elif list_row > 8:
            list_row = 0

        if list_col < 0:
            list_col = 8
        elif list_col > 8:
            list_col = 0

        new_current_cell = self.cells[list_row][list_col]
        new_current_cell.highlight()
        self.current_cell = new_current_cell

    def solve(self):
        self.is_solved = True
        solver = SudokuSolver(self.cells, self.squares)

    def reset_board(self):
        self.is_solved = False
        for row in self.cells:
            for cell in row:
                self.canvas.delete(cell.unique_tag)
                cell.value = None
                cell.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class Cell:
    def __init__(self, board, list_coord, x1, y1, x2, y2):
        self.value = None
        self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.list_coord = list_coord
        self.canvas = board
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.unique_tag = f'cell{self.x1}{self.y1}'  # Cannot be digit-only

    def highlight(self):
        self.canvas.delete('highlight')
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, tags='highlight', outline='RoyalBlue2',
                                     width=7)

    def show_digit(self, digit, color):
        self.canvas.delete(self.unique_tag)
        x = self.x1 + SIDE / 2
        y = self.y1 + SIDE / 2
        self.value = digit
        self.canvas.create_text(x, y, text=str(digit), tags=self.unique_tag, fill=color, font=('Script', 15, 'bold'))


root = Tk()
root.title("Sudoku Solver")
root.geometry(f'{int(WIDTH * 1)}x{int(HEIGHT * 1.05)}')

app = Board(root)

root.mainloop()
