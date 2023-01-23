from tkinter import *

SIDE = 100
WIDTH = 9 * SIDE
HEIGHT = WIDTH

class Board(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.draw_grid()

    def draw_grid(self):
        for line_nr in range(10):
            # change color for every 3rd line:
            color = 'grey'
            line_width = 1
            if line_nr % 3 == 0:
                color = 'black'
                line_width = 3
            # draw vertical lines:
            y1 = 0
            y2 = HEIGHT
            x = line_nr * SIDE
            self.canvas.create_line(x, y1, x, y2, fill=color, width=line_width)

            # draw horizontal lines:
            x1 = 0
            x2 = WIDTH
            y = line_nr * SIDE
            self.canvas.create_line(x1, y, x2, y, fill=color, width=line_width)



root = Tk()
root.title("Sudoku Solver")
root.geometry(f'{WIDTH}x{HEIGHT}')
app = Board(root)


root.mainloop()