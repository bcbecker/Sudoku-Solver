#Grid class, sets up board grid

import pygame
from Box import Box
from main_helpers import is_valid, find_empty


class Grid:
    """
    Sets up the board and associated methods using the Box class
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
        self.model = [[self.boxes[x][y].value for y in range(self.cols)] for x in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set(val)
            self.update_model()

            if is_valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.boxes[row][col].set(0)
                self.boxes[row][col].set_temp_entry(0)
                self.update_model()
                return False

    def sketch_entry(self, val):
        row, col = self.selected
        self.boxes[row][col].set_temp_entry(val)

    def draw_board(self):
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
        # Reset all other
        for x in range(self.rows):
            for y in range(self.cols):
                self.boxes[x][y].selected = False

        self.boxes[row][col].selected = True
        self.selected = (row, col)

    def clear_entry(self):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set_temp_entry(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.boxes[x][y].value == 0:
                    return False
        return True

    def solve(self):
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
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if is_valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.boxes[row][col].set(i)
                self.boxes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_board():
                    return True

                self.model[row][col] = 0
                self.boxes[row][col].set(0)
                self.update_model()
                self.boxes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False
