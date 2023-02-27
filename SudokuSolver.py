class SudokuSolver:
    def __init__(self, rows, columns, squares):
        self.cluster_types = [rows, columns, squares]
        self.check_board_validity()
        self.updates_done = 0  # Used to determine whether the solving algorithms are advancing
        self.initial_analysis()

    def check_board_validity(self):
        for clusters_type in self.cluster_types:
            for cluster in clusters_type:
                values = []
                for cell in cluster:
                    if cell.value:
                        if cell.value in values:
                            raise Exception('Board is invalid!')
                        else:
                            values.append(cell.value)

    def initial_analysis(self):
        for row in self.cluster_types[0]:
            for cell in row:
                if cell.value:
                    self.update_cells(cell)

    def check_if_solved(self):
        for row in self.cluster_types[0]:
            for cell in row:
                if not cell.value:
                    return False
        return True

    def solve(self):
        # !!! if a cell is solved, it has to have only 1 value in cell.possible_values !!!
        # while not self.check_if_solved():
        self.updates_done = 0
        print(self.cluster_types[0][7][0].possible_values)

        self.check_singles()
        # self.check_hidden_singles()
        # if self.updates_done == 0:
            # self.check_pairs()
            # self.check_triples()
            # self.check_pointing_pairs()

        print(self.cluster_types[0][7][0].possible_values)
        # if self.updates_done == 0:  # temporary
        # show_pop_up('Error', 'This puzzle is unsolvable!')
        # break

    def check_singles(self):
        for clusters_type in self.cluster_types:
            for cluster in clusters_type:
                for cell in cluster:
                    if not cell.value:
                        if len(cell.possible_values) == 1:
                            digit = cell.possible_values[0]
                            cell.show_digit(digit, 'slate grey')
                            self.update_cells(cell)

    def check_pairs(self):
        for clusters_type in self.cluster_types:
            for cluster in clusters_type:
                for cell in cluster:
                    values = cell.possible_values
                    if len(cell.possible_values) == 2:
                        other_cells = cluster.copy()
                        other_cells.remove(cell)
                        for other_cell in other_cells:
                            if cell.possible_values == other_cell.possible_values:
                                other_cells.remove(other_cell)
                                self.update_cells(cell, other_cells, values)
                                break

    def check_triples(self):
        for clusters_type in self.cluster_types:
            for cluster in clusters_type:
                for cell in cluster:
                    if len(cell.possible_values) == 2:
                        other_cells = cluster.copy()
                        other_cells.remove(cell)
                        for second_cell in other_cells:
                            set_1 = set(cell.possible_values)
                            set_2 = set(second_cell.possible_values)
                            set_3 = None
                            if len(set_2) == 2 and set_1 & set_2:
                                other_cells.remove(second_cell)
                                for third_cell in other_cells:
                                    set_3 = set(third_cell.possible_values)
                                    if len(set_3) == 2 and set_1 & set_3 and set_2 & set_3:
                                        other_cells.remove(third_cell)
                                        values = list(set_1 | set_2 | set_3)
                                        self.update_cells(cell, other_cells, values)
                                        break
                            if set_3:
                                break

    def check_hidden_singles(self):
        for clusters_type in self.cluster_types:
            for cluster in clusters_type:
                empty_cluster_cells = cluster.copy()

                # Find all cells in a cluster that are still to be solved:
                for cell in cluster:
                    if cell.value:
                        empty_cluster_cells.remove(cell)

                # Get empty cells excluding the one that is currently analysed:
                for cell in empty_cluster_cells:
                    other_cells = empty_cluster_cells.copy()
                    other_cells.remove(cell)

                    # Check if any digit in the cell, is single in the cluster:
                    for value in cell.possible_values:
                        is_single = True
                        for other_cell in other_cells:
                            if value in other_cell.possible_values:
                                is_single = False
                                break
                        if is_single:
                            cell.possible_values = [value]
                            cell.show_digit(value, 'green')
                            self.update_cells(cell)

    def check_hidden_pairs(self):
        pass

    def check_hidden_triples(self):
        pass

    def check_pointing_pairs(self):
        squares = self.cluster_types[2]
        for square in squares:

            # Get remaining empty cells and values in a square:
            empty_square_cells = square.copy()
            possible_values = list(range(1, 10))
            for cell in square:
                if cell.value:
                    possible_values.remove(cell.value)
                    empty_square_cells.remove(cell)

            # Check if any value can only be in two cells within a square:
            for possible_value in possible_values:
                decisive_cells = []
                for empty_cell in empty_square_cells:
                    if len(decisive_cells) > 2:
                        break
                    elif possible_value in empty_cell.possible_values:
                        decisive_cells.append(empty_cell)

                # Check if the values are in the same row or column:
                if len(decisive_cells) == 2:
                    # Rows:
                    if decisive_cells[0].list_coord[0] == decisive_cells[1].list_coord[0]:
                        row_id = decisive_cells[0].list_coord[0]
                        other_row_cells = self.cluster_types[0][row_id].copy()
                        for decisive_cell in decisive_cells:
                            other_row_cells.remove(decisive_cell)
                        self.update_cells(decisive_cells[0], other_row_cells, [possible_value])
                    # Columns:
                    elif decisive_cells[0].list_coord[1] == decisive_cells[1].list_coord[1]:
                        column_id = decisive_cells[0].list_coord[1]
                        other_column_cells = self.cluster_types[1][column_id].copy()
                        for decisive_cell in decisive_cells:
                            other_column_cells.remove(decisive_cell)
                        self.update_cells(decisive_cells[0], other_column_cells, [possible_value])

    def check_pointing_triples(self):
        pass

    def check_x_wing(self):
        pass

    def check_y_wing(self):
        pass

    def check_swordfish(self):
        pass

    def update_cells(self, cell, influence_cells=None, values=None):
        if cell.value:
            value = cell.value
            row = self.cluster_types[0][cell.list_coord[0]]
            column = self.cluster_types[1][cell.list_coord[1]]
            square = self.cluster_types[2][cell.square_id]
            influence_clusters = [row, column, square]
            for cluster in influence_clusters:
                for cell in cluster:
                    if not cell.value:
                        if value in cell.possible_values:
                            cell.possible_values.remove(value)
                            self.updates_done += 1
        else:
            for value in values:
                for influence_cell in influence_cells:
                    if not influence_cell.value:
                        if value in influence_cell.possible_values:
                            influence_cell.possible_values.remove(value)
                            self.updates_done += 1
