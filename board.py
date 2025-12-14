import cell

# Information used in this file:
# The cells list to be seen is used to contain the cells of the board (small boards or x/o spaces)
# The board indexes are as follows:
# 0     1      2
# 3     4      5
# 6     7      8


class Board:
    def __init__(self, start_x, start_y, board, line_horizontal, line_vertical, line_diagonal_l,
                 line_diagonal_r):

        self.won = (cell.XO.blank, None, None)  # (who won, first cell index, which type of line)

        # Coordinates
        self.start_x = start_x
        self.start_y = start_y

        # Images
        self.board = board
        self.line_horizontal = line_horizontal
        self.line_vertical = line_vertical
        self.line_diagonal_l = line_diagonal_l
        self.line_diagonal_r = line_diagonal_r

        self.cells = []     # Cells to be filled in

    def draw(self, screen):
        pass

    # Check for winner and put in self.won variable
    def winner(self):
        pass

    # Check if board is full
    def full(self):
        pass

    # Receive x, y coordinates on screen return which cell is in those coordinates
    def find(self, x, y):
        pass


class SmallBoard(Board):

    def __init__(self, start_x, start_y, x_distance, y_distance, board, small_x, small_o,
                 line_horizontal, line_vertical, line_diagonal_l, line_diagonal_r):

        Board.__init__(self, start_x, start_y, board, line_horizontal, line_vertical,
                       line_diagonal_l, line_diagonal_r)

        # Distance from start_y or start_x to the first, second and third row/column
        self.x_distance = x_distance
        self.y_distance = y_distance

        for i in range(3):
            for j in range(3):
                self.cells.append(cell.Cell(start_x + j*self.x_distance, start_y + i*self.y_distance, small_x, small_o))

    def winner(self):
        if self.won[0] != cell.XO.blank:
            return

        # check horizontal
        for i in range(0, 9, 3):
            if self.cells[i].id == self.cells[i+1].id and self.cells[i].id == self.cells[i+2].id and \
                    self.cells[i].id is not cell.XO.blank:
                self.won = (self.cells[i].id, i, self.line_horizontal)
                return

        # check vertical
        for i in range(3):
            if self.cells[i].id == self.cells[i+3].id and self.cells[i].id == self.cells[i+6].id \
                    and self.cells[i].id is not cell.XO.blank:
                self.won = (self.cells[i].id, i, self.line_vertical)
                return

        # check diagonals
        if self.cells[0].id == self.cells[4].id and self.cells[0].id == self.cells[8].id \
                and self.cells[0].id is not cell.XO.blank:
            self.won = (self.cells[0].id, 0, self.line_diagonal_l)
            return
        if self.cells[2].id == self.cells[4].id and self.cells[2].id == self.cells[6].id \
                and self.cells[2].id is not cell.XO.blank:
            self.won = (self.cells[2].id, 0, self.line_diagonal_r)      # the first cell is 0 for drawing purposes
            return

    # get coordinates and return the index of the cell in those coordinates
    def find(self, x, y):
        # Check if the chosen square is out of bounds
        if x < self.start_x or y < self.start_y or x > (self.start_x + self.x_distance*2 + cell.Cell.length) or \
                y > (self.start_y + self.y_distance*2 + cell.Cell.height):
            return None

        # Finding the cell
        column = 0
        while column in range(3):
            if x < (self.start_x + self.x_distance * column + cell.Cell.length):
                break
            column += 1

        row = 0
        while row in range(3):
            if y < (self.start_y + self.y_distance*row + cell.Cell.height):
                break
            row += 1

        return row*3 + column

    def draw(self, screen):
        screen.blit(self.board, (self.start_x, self.start_y))
        self.winner()
        for i in self.cells:
            i.draw(screen)
        (winner, where, line) = self.won

        if winner != cell.XO.blank:
            screen.blit(line, (self.cells[where].start_x, self.cells[where].start_y))

    def full(self):
        for i in self.cells:
            if i.id == cell.XO.blank:
                return False
        return True


class BigBoard(Board):

    def __init__(self, start_x, start_y, x_distance, y_distance, board, big_x,
                 big_o, line_horizontal, line_vertical, line_diagonal_l, line_diagonal_r, s_board, small_x, small_o,
                 s_horizontal, s_vertical, s_diagonal_l, s_diagonal_r):
        Board.__init__(self, start_x, start_y, board,
                       line_horizontal, line_vertical, line_diagonal_l, line_diagonal_r)

        self.big_x = big_x
        self.big_o = big_o

        # creating 9 boards in the cell array
        for i in range(3):
            for j in range(3):
                self.cells.append(SmallBoard(self.start_x+j*x_distance, self.start_y+i*y_distance, 75, 65, s_board,
                                             small_x, small_o, s_horizontal, s_vertical, s_diagonal_l, s_diagonal_r))

    def draw(self, screen, show_score=False):
        screen.blit(self.board, (self.start_x, self.start_y))

        if show_score:
            for i in self.cells:
                if i.won[0] == cell.XO.x:
                    screen.blit(self.big_x, (i.start_x, i.start_y))
                elif i.won[0] == cell.XO.o:
                    screen.blit(self.big_o, (i.start_x, i.start_y))
                # draw winning line if exists
                if self.won[0] != cell.XO.blank:
                    screen.blit(self.won[2], (self.cells[self.won[1]].start_x, self.cells[self.won[1]].start_y))
        else:
            for i in self.cells:
                i.draw(screen)

    # x, y - position on the screen
    # return value - the index of the small board in that location and the index of the cell in the board
    def find(self, x, y):
        chosen = False  # if a cell has been chosen
        i = 0
        tiny_index = 0  # the potential index of the cell inside the small board
        while i < len(self.cells) and not chosen:
            tiny_index = self.cells[i].find(x, y)
            chosen = tiny_index is not None
            i += 1

        if not chosen:
            return None
        return i-1, tiny_index

    def winner(self):
        if self.won[0] != cell.XO.blank:
            return

        # check horizontal
        for i in [0, 3, 6]:
            if self.cells[i].won[0] == self.cells[i+1].won[0] and self.cells[i].won[0] == self.cells[i+2].won[0]:
                self.won = (self.cells[i].won[0], i, self.line_horizontal)
                return

        # check vertical
        for i in range(3):
            if self.cells[i].won[0] == self.cells[i+3].won[0] and self.cells[i].won[0] == self.cells[i+6].won[0]:
                self.won = (self.cells[i].won[0], i, self.line_vertical)
                return

        # check diagonals
        if self.cells[0].won[0] == self.cells[4].won[0] and self.cells[0].won[0] == self.cells[8].won[0]:
            self.won = (self.cells[0].won[0], 0, self.line_diagonal_l)
            return
        if self.cells[2].won[0] == self.cells[4].won[0] and self.cells[2].won[0] == self.cells[6].won[0]:
            self.won = (self.cells[2].won[0], 0, self.line_diagonal_l)      # the first cell is 0 for drawing purposes
            return

    # cell in board big_i in cell small_i turns into x/o
    def choose(self, big_i, small_i, xo):
        if big_i is None or small_i is None or self.cells[big_i].cells[small_i].id is not cell.XO.blank:
            return False
        self.cells[big_i].cells[small_i].id = xo
        return True

    def full(self):
        for i in self.cells:
            if not i.full():
                return False
        return True
