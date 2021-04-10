#Box class, sets up each box

import pygame
pygame.font.init()


class Box:
    """
    Sets up the board boxes and associated utility methods
    """
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        """
        Sets up necessary variables for defined board
        :param value: int
        :param row: int
        :param col: int
        :param width: int
        :param height: int
        :return: None
        """
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """
        Draws out lines for board
        :param win: pygame obj
        :return: None
        """
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        """
        Shows the logic of the board solving
        :param win: pygame obj
        :param g: bool
        :return: None
        """
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set_entry(self, val):
        """
        Simple setter for the value to be placed in Grid
        :param val: int
        :return: None
        """
        self.value = val

    def set_temp_entry(self, val):
        """
        Simple setter for the value to be checked
        :param val: int
        :return: None
        """
        self.temp = val
