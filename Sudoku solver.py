from tkinter import *

SIDE = 100
MARGIN = 50
WIDTH = 9 * SIDE + 2 * MARGIN
HEIGHT = WIDTH


class Board(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.draw_grid()
        self.cells = []
        self.create_cells()
        self.cells[0][0].highlight()

        self.canvas.bind("<Button-1>", self._choose_cell)
        self.canvas.bind("<Key>", self._choose_digit)

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
        for col_nr in range(9):
            row = []

            for row_nr in range(9):
                x1 = MARGIN + row_nr * SIDE
                y1 = MARGIN + col_nr * SIDE
                x2 = x1 + SIDE
                y2 = y1 + SIDE
                cell = Cell(self.canvas, x1, y1, x2, y2)
                row.append(cell)

            self.cells.append(row)


    def _choose_cell(self, coord):
        pass

    def _create_text_fields(self, row, col, digit):
        pass

    def _choose_digit(self, event):
        pass


class Cell:
    def __init__(self, board, x1, y1, x2, y2):
        self.canvas = board
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def highlight(self):
        self.canvas.delete('highlight')
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, tags='highlight', outline='green', width=5)


root = Tk()
root.title("Sudoku Solver")
root.geometry(f'{WIDTH}x{HEIGHT}')
app = Board(root)

root.mainloop()
