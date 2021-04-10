#Grid class, sets up board grid

import pygame
from Box import Box
from main_helpers import is_valid, find_empty


class Grid:
    """
    Sets up the board grid and associated utility methods using the Box class
    """
    board = [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 6, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, win):
        """
        Sets up necessary variables for defined board
        :param rows: int
        :param cols: int
        :param width: int
        :param height: int
        :param win: pygame obj
        :return: None
        """
        self.rows = rows
        self.cols = cols
        self.boxes = [[Box(self.board[x][y], x, y, width, height) for y in range(cols)] for x in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        """
        Reinitializes the boxes for each iteration
        """
        self.model = [[self.boxes[x][y].value for y in range(self.cols)] for x in range(self.rows)]

    def place(self, val):
        """
        Places/validates an entry made
        :param val: int
        :return: bool
        """
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set_entry(val)
            self.update_model()

            if is_valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.boxes[row][col].set_entry(0)
                self.boxes[row][col].set_temp_entry(0)
                self.update_model()
                return False

    def sketch_entry(self, val):
        """
        Places temp entry made my user, yet to be validated
        :param val: int
        :return: None
        """
        row, col = self.selected
        self.boxes[row][col].set_temp_entry(val)

    def draw_board(self):
        """
        Draws structure of the game board
        """
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw boxes
        for x in range(self.rows):
            for y in range(self.cols):
                self.boxes[x][y].draw(self.win)

    def select(self, row, col):
        """
        Higlights/allows entry in selected box
        :param row: int
        :param col: int
        :return: None
        """
        # Reset all other
        for x in range(self.rows):
            for y in range(self.cols):
                self.boxes[x][y].selected = False

        self.boxes[row][col].selected = True
        self.selected = (row, col)

    def clear_entry(self):
        """
        For backspace entry, to remove the temp entry
        """
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set_temp_entry(0)

    def click(self, pos):
        """
        Position of the mouse click on the 2d array that is the board
        :param pos: pygame obj
        :return: (int, int)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None
    
    def test_arrows(self, pos, direction):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            if (direction == 'U'):
                return (int(y+1),int(x))
            elif (direction == 'D'):
                return (int(y-1),int(x))
            elif (direction == 'L'):
                return (int(y),int(x-1))
            if (direction == 'R'):
                return (int(y),int(x+1))
        else:
            return None

    def is_finished(self):
        """
        Checks if the board has any incomplete/empty boxes
        :param: None
        :return: bool
        """
        for x in range(self.rows):
            for y in range(self.cols):
                if self.boxes[x][y].value == 0:
                    return False
        return True

    def solve(self):
        """
        Checks that the entry is in the correct box
        :param: None
        :return: bool
        """
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if is_valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_board(self):
        """
        Backtracks to solve the remaining empty boxes, completes board
        :param: None
        :return: bool
        """
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if is_valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.boxes[row][col].set_entry(i)
                self.boxes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_board():
                    return True

                self.model[row][col] = 0
                self.boxes[row][col].set_entry(0)
                self.update_model()
                self.boxes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False
