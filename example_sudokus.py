EASY_BOARD = [[9, 3, 4, 1, 8, 2, 5, 6, None],
              [2, None, None, None, None, None, None, None, None],
              [8, 6, 1, 7, 3, 5, 4, None, None],
              [None, 2, 8, None, None, 7, None, 4, None],
              [None, 7, 6, None, None, 8, 9, 2, 1],
              [5, None, 9, 4, 2, 6, 3, 7, 8],
              [6, 9, 5, None, None, None, 8, None, None],
              [7, 8, None, 5, 4, 9, 2, None, 6],
              [1, None, None, None, 6, 3, 7, 5, None]]
medium_board = [[], [], [], [], [], [], [], [], []]
hard_board = [[], [], [], [], [], [], [], [], []]
very_hard_board = [[], [], [], [], [], [], [], [], []]


def load_board(cells, board):
    for row_nr in range(9):
        for col_nr in range(9):
            digit = board[row_nr][col_nr]
            cell = cells[row_nr][col_nr]
            cell.value = digit
            if digit is not None:
                cell.show_digit(digit, 'black')
