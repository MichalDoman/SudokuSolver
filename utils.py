def load_board(cells, board):
    for row_nr in range(9):
        for col_nr in range(9):
            digit = board[row_nr][col_nr]
            cell = cells[row_nr][col_nr]
            cell.value = digit
            if digit is not None:
                cell.show_digit(digit)
                cell.possible_values = []
                