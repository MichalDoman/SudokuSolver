from tkinter import *
from SudokuSolver import SudokuSolver
from utils import load_board
from sudoku_boards import *

# Settings:
SIDE = 100
MARGIN = 50
WIDTH = 9 * SIDE + 2 * MARGIN
HEIGHT = WIDTH

BOARD_TO_LOAD = EXPERT_BOARD_2


class Board(Frame):
    """
    This class is the main frame of the application which holds the whole content.
    It contains functions which draw Sudoku board and all necessary components as well as
    methods that allow the user to perform actions within the app. Sudoku board is divided
    into 9x9 cells, and cells are segregated by clusters, which are rows, columns and 3x3 squares.
    """
    def __init__(self, master):
        """
        Create canvas and add all necessary widgets to it.
        Create all functionalities like key bindings, movement on the Sudoku grid and typing digits.
        Create and segregate cells into clusters (necessary for the Solver).
        Add buttons functionalities, and save action history for undoing.

        :param master main window of the application (root), to which the Board instance is assigned.
        """
        super().__init__(master)
        # Prepare canvas and widgets:
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=RIGHT)

        self.solve_button = Button(self, text='Solve', width=24, bd=3, bg='chartreuse4', fg='white',
                                   activebackground='dark green', activeforeground='white', font=('Script', 10, 'bold'),
                                   relief="flat", command=self.solve)
        self.solve_button.pack(fill=BOTH, expand=True, side=TOP)

        self.undo_button = Button(self, text='Undo', width=24, bd=3, bg='RoyalBlue2', fg='white',
                                  activebackground='RoyalBlue3', activeforeground='white', font=('Script', 10, 'bold'),
                                  relief="flat", command=self.undo)
        self.undo_button.pack(fill=BOTH, expand=True, side=TOP)

        self.clear_button = Button(self, text='Clear', width=24, bd=3, bg='DarkGoldenrod2', fg='white',
                                   activebackground='DarkGoldenrod3', activeforeground='white',
                                   font=('Script', 10, 'bold'),
                                   relief="flat", command=self.clear_board)
        self.clear_button.pack(fill=BOTH, expand=True, side=TOP)

        self.reset_button = Button(self, text='Reset', width=24, bd=3, bg='OrangeRed3', fg='white',
                                   activebackground='OrangeRed4', activeforeground='white', font=('Script', 10, 'bold'),
                                   relief="flat", command=self.reset_board)
        self.reset_button.pack(fill=BOTH, expand=True, side=TOP)

        self.auto_cell_switch = IntVar()
        self.checkbox = Checkbutton(self, text='Auto Cell Switch: ON', relief='flat', variable=self.auto_cell_switch,
                                    bd=0, pady=20, bg='dim grey',
                                    fg='white', activebackground='dim grey', activeforeground='white',
                                    selectcolor='dim grey', font=('Script', 8, 'bold'), indicatoron=False,
                                    justify=CENTER, command=self.change_checkbutton_label)
        self.checkbox.pack(fill=BOTH)

        # Create cells and organise them:
        self.draw_grid()
        self.cells = []  # Used as 'rows' in Solver
        self.columns = []
        self.squares = []
        self.create_cells()
        self.create_columns()
        self.create_squares()
        self.current_cell = self.cells[0][0]
        self.current_cell.highlight()
        load_board(self.cells, BOARD_TO_LOAD)  # used for testing

        # Miscellaneous:
        self.undo_list = []  # stores every action for undo function
        self.is_solved = False
        self.is_auto_switching = True

        # Bind necessary keys:
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.choose_cell)
        self.canvas.bind("<Key>", self.choose_digit)
        self.canvas.bind("<Up>", self.switch_cells_with_arrows)
        self.canvas.bind("<Down>", self.switch_cells_with_arrows)
        self.canvas.bind("<Left>", self.switch_cells_with_arrows)
        self.canvas.bind("<Right>", self.switch_cells_with_arrows)
        self.canvas.bind("<space>", lambda key_press: self.delete_digit())
        self.canvas.bind("<BackSpace>", lambda key_press: self.undo())
        self.canvas.bind("<Control-z>", lambda key_press: self.undo())

    def draw_grid(self):
        """
        Draw a 9x9 Sudoku grid on the canvas. Every third line starting from the first line
        of the grid's rows and columns is bold.
        """
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
        """
        Create an instance of Cell class for every square of the grid and assign coordinates.
        Append all the cells to the list (segregated by rows).
        """
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

    def create_columns(self):
        """Reorganise cells into a list of columns."""
        for col_nr in range(len(self.cells)):
            column = []
            for row in self.cells:
                cell_in_column = row[col_nr]
                column.append(cell_in_column)
            self.columns.append(column)

    def create_squares(self):
        """Reorganise cells into a list of 3x3 squares."""
        square_id = 0
        for square_x in range(0, 9, 3):  # for 0, 3 and 6
            for square_y in range(0, 9, 3):
                square = []
                for row in range(square_x, square_x + 3):  # (0, 3), (3, 6) and (6, 9)
                    for col in range(square_y, square_y + 3):
                        cell = self.cells[row][col]
                        cell.square_id = square_id
                        square.append(cell)
                self.squares.append(square)
                square_id += 1

    def choose_cell(self, click_coord):
        """
        Highlight and select cell as current with mouse click.
        :param click_coord: window coordinates of LMB click
        """
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
        """
        Display a digit typed by the user if the board is not solved.
        Update undo list with typing-a-digit action.
        Set possible values for the filled cell as an empty list.
        Removes previous value if existed.

        :param key_press: a value of a key pressed. Only digits from 1 to 9 pass the conditions.
        """
        if not self.is_solved:
            key_char = key_press.char
            if key_char.isdigit() and int(key_char) != 0:
                # update undo_list with the current action
                if int(key_char) != self.current_cell.value:
                    previous_cell = self.current_cell
                    previous_value = self.current_cell.value
                    self.undo_list.append(('value', previous_cell, previous_value))

                self.current_cell.show_digit(int(key_char), 'black')
                self.current_cell.possible_values = []
                self.auto_switch()

    def change_checkbutton_label(self):
        """
        Turn auto-switch off and on.
        Change button label according to settings.
        """
        if self.auto_cell_switch.get():
            self.checkbox['text'] = 'Auto Cell Switch: OFF'
            self.is_auto_switching = False
        else:
            self.checkbox['text'] = 'Auto Cell Switch: ON'
            self.is_auto_switching = True

    def auto_switch(self):
        """
        After typing a digit automatically jup to the next cell.
        If current cell is utmost, jump to the first cell of the next row.
        """
        if self.is_auto_switching:
            if self.current_cell.list_coord[1] == 8:
                self.switch_cells_with_arrows('Right')
                self.switch_cells_with_arrows('Down')
            else:
                self.switch_cells_with_arrows('Right')

    def delete_digit(self):
        """
        Remove a digit display from cell.
        Change cell variables to that of an empty cell.
        Update undo list with digit-removing action.
        """
        if not self.is_solved:
            # update undo_list with the current action
            if self.current_cell.value is not None:
                previous_cell = self.current_cell
                previous_value = self.current_cell.value
                self.undo_list.append(('value', previous_cell, previous_value))

                self.canvas.delete(self.current_cell.unique_tag)
                self.current_cell.value = None
                self.current_cell.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.auto_switch()

    def switch_cells_with_arrows(self, arrow_press):
        """
        Enable switching cells with arrows. At utmost positions switch to first cell of next row.
        Set new current cell after switch.
        Enable auto-move directly through code.

        :param arrow_press: can be a string representing arrow-key symbol while calling the method from code
        or a key symbol if clicked by the user.
        """
        # Adjust for auto_switch function:
        if isinstance(arrow_press, str):
            arrow = arrow_press
        else:
            arrow = arrow_press.keysym

        # Function's main body:
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
        """
        Assigned for solving button. Create an instance of SudokuSolver class which solves
        the Board while initiated.
        Add solving action to undo list.
        Change Board status to "solved".
        Show exception for invalid board which is raised by the Solver. If an exception occurs,
        clear the board.
        """
        # try:
        solver = SudokuSolver(self.cells, self.columns, self.squares)
        solver.solve()
        # update undo_list with the current action
        if not self.is_solved:
            self.undo_list.append(('solve',))

        self.is_solved = True

        # except Exception as inst:
        #     print(inst.args[0])
        #     self.clear_board()

    def undo(self):
        """Depending on the type of action saved in the undo list, reset the state of the board."""
        if self.undo_list:
            last_move = self.undo_list[-1]

            if last_move[0] == 'value':
                new_current_cell = last_move[1]
                new_value = last_move[2]

                new_current_cell.highlight()
                self.current_cell = new_current_cell
                self.current_cell.value = new_value
                if new_value:
                    self.current_cell.show_digit(new_value)
                else:
                    self.current_cell.reset()

            elif last_move[0] == 'clear':
                self.solve()
                self.undo_list.pop(-1)  # removes two items from the list since self.solve adds an extra one

            elif last_move[0] == 'solve':
                self.clear_board()
                self.undo_list.pop(-1)  # -//-


            elif last_move[0] == 'reset':
                new_board = last_move[1]
                was_solved = False  # checks for 'solve + reset' situation
                for row_nr in range(9):
                    for col_nr in range(9):
                        digit = new_board[row_nr][col_nr]
                        cell = self.cells[row_nr][col_nr]
                        if cell.possible_values != 9:
                            was_solved = True
                        cell.value = digit
                        if digit is not None:
                            cell.show_digit(digit)
                        else:
                            cell.reset()
                if was_solved:
                    self.undo_list.pop(-1)

            self.undo_list.pop(-1)

    def clear_board(self):
        """Clear the board from solved digits (initially inserted digits remain) and update undo list."""
        self.is_solved = False
        is_cleared = False

        for row in self.cells:
            for cell in row:
                if len(cell.possible_values) == 1:
                    is_cleared = True
                    cell.reset()

        # update undo_list with the current action
        if is_cleared:
            self.undo_list.append(('clear',))

    def reset_board(self):
        """Reset the Board to an empty state and update undo list."""
        self.is_solved = False

        # update undo_list with the current action:
        previous_board = []
        for row in self.cells:
            previous_row = []
            for col_nr in range(len(row)):
                cell = row[col_nr]
                if len(cell.possible_values) != 9:  # if a cell was solved by the solver
                    value = None
                else:
                    value = cell.value
                previous_row.append(value)
            previous_board.append(previous_row)
        self.undo_list.append(('reset', previous_board))

        # reset board:
        for row in self.cells:
            for cell in row:
                cell.reset()


class Cell:
    """A class representing a single cell on the sudoku Board."""
    def __init__(self, board, list_coord, x1, y1, x2, y2):
        """
        Set cell's attributes.

        :param board: instance of Board class.
        :param list_coord: row and column indexes from Board's cells list (by rows).
        :param x1: x coordinate of top-left edge within the app window
        :param y1: y coordinate of top-left edge within the app window
        :param x2: x coordinate of bottom-right left edge within the app window
        :param y2: y coordinate of bottom-right edge within the app window
        """
        self.value = None
        self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.list_coord = list_coord
        self.square_id = None  # square index from cells list segregated by 3x3 squares
        self.canvas = board
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.unique_tag = f'cell{self.x1}{self.y1}'  # Cannot be digit-only

    def highlight(self):
        """Draw a rectangle on cell's borders to highlight it. Delete previous highlight."""
        self.canvas.delete('highlight')
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, tags='highlight', outline='RoyalBlue2',
                                     width=7)

    def show_digit(self, digit, color='black'):
        """
        Delete previous currently displayed value and draw a new text widget.
        Deletion is based on a unique tags assigned to digits in every cell.
        """
        self.canvas.delete(self.unique_tag)
        x = self.x1 + SIDE / 2
        y = self.y1 + SIDE / 2
        self.value = digit
        self.canvas.create_text(x, y, text=str(digit), tags=self.unique_tag, fill=color, font=('Script', 15, 'bold'))

    def reset(self):
        """Reset cell's values to that of an empty cell"""
        self.value = None
        self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.canvas.delete(self.unique_tag)

    def __str__(self):
        return self.list_coord


def show_pop_up(title, label_text, button_text='OK'):
    pop_up = Toplevel(root)
    pop_up.geometry(f'{int(WIDTH * 0.7)}x{int(HEIGHT * 0.3)}')
    pop_up.title(title)
    Label(pop_up, text=label_text, font=('Script', 16, 'bold')).place(relx=0.5, rely=0.3, anchor='center')
    Button(pop_up, width=25, height=2, text=button_text, bg='chartreuse4', fg='white',
           activebackground='dark green', activeforeground='white', font=('Script', 10, 'bold'),
           relief="flat", command=pop_up.destroy).place(relx=0.5, rely=0.65, anchor='center')


root = Tk()
root.title("Sudoku Solver")
root.geometry(f'{int(WIDTH * 1.3)}x{HEIGHT}')

app = Board(root)

root.mainloop()
