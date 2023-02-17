TEST_BOARD = [[1, None, None, 3, None, None, 5, None, 9],
              [2, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, 4, None, None, None, None, None, None],
              [None, None, None, None, 4, None, None, None, None],
              [None, None, None, None, None, None, 4, None, None],
              [5, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, 4, None],
              [None, None, None, 4, None, None, None, None, None]]

EMPTY_BOARD = [[None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None]]

MEDIUM_BOARD = [[None, 5, 4, 6, None, None, 8, 3, 7],
                [6, 8, 2, 5, None, None, None, None, None],
                [None, 3, 9, 4, 1, 8, 2, 6, None],
                [None, None, None, 2, 8, 5, 7, 9, None],
                [None, None, None, 9, 4, 7, 6, 8, 3],
                [None, 7, 8, None, None, None, 5, 4, None],
                [8, 9, 7, None, None, None, None, None, None],
                [None, 6, None, None, None, 1, 9, 2, 8],
                [None, None, 5, None, None, 9, None, None, None]]

HARD_BOARD = [[None, None, 7, None, None, 8, None, None, 6],
              [4, 8, 3, 6, None, None, None, 2, 7],
              [2, 6, None, 3, None, None, 4, None, 8],
              [5, 3, None, 9, 6, None, None, None, None],
              [None, None, None, None, None, None, 5, 3, 9],
              [7, 9, None, 1, None, None, 8, None, None],
              [6, None, None, None, 2, 3, 7, 8, 1],
              [None, None, None, None, None, 6, 2, 9, 5],
              [None, 2, None, None, 7, 9, None, None, None]]

EXPERT_BOARD = [[None, 1, None, None, 2, 9, None, None, None],
                [None, None, 7, None, None, None, None, 5, 6],
                [5, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, 8, None, 4, None],
                [None, None, None, None, 6, 4, 2, 9, None],
                [7, None, 5, 9, None, None, None, None, None],
                [9, 8, None, None, None, None, 3, None, None],
                [None, None, None, None, None, 7, None, None, None],
                [None, None, None, None, None, None, None, 6, 1]]

VERY_HARD_BOARD = [[None, 8, 2, None, None, None, None, None, None],
                   [None, 7, None, None, 1, None, None, None, None],
                   [None, None, None, None, None, None, 9, None, None],
                   [6, None, None, None, 3, None, 4, 5, None],
                   [ None, None, None, None, None, 8, None, None, 7],
                   [9,  None, None, None, None, None, None, None, None],
                   [ None, None, None, 7, None, 2, None, None, None],
                   [None, None, None, None, None, None, 6, 3, None],
                   [None, None, None, 8, None, None, None, None, None]]


def load_board(cells, board):
    for row_nr in range(9):
        for col_nr in range(9):
            digit = board[row_nr][col_nr]
            cell = cells[row_nr][col_nr]
            cell.value = digit
            if digit is not None:
                cell.show_digit(digit)
                cell.possible_values = []
