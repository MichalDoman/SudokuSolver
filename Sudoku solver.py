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
        self.current_cell = None

        self.canvas.bind("<Button-1>", self.choose_cell)
        self.bind("<Key>", self.choose_digit)


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

    @staticmethod
    def choose_digit(event):
        print(event.keysym)
        # if self.current_cell:
        #     # if key.char in "123456789":
        #     print(self.current_cell)
        #     print(key.char)
        #     self.current_cell.show_digit(int(key.char))

    def reset_board(self):
        pass

class Cell:
    def __init__(self, board, x1, y1, x2, y2):
        self.value = None
        self.canvas = board
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def highlight(self):
        self.canvas.delete('highlight')
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, tags='highlight', outline='green', width=7)

    def show_digit(self, digit):
        x = self.x1 + SIDE / 2
        y = self.y1 + SIDE / 2
        self.value = digit
        self.canvas.create_text(x, y, text=str(digit), tags='digit', font=('Script', 15, 'bold'))


root = Tk()
root.title("Sudoku Solver")
root.geometry(f'{int(WIDTH * 1)}x{HEIGHT}')

app = Board(root)

root.mainloop()
