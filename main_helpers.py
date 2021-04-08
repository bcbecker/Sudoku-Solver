# Main logic helper functions
import pygame

def find_empty(bo):
    for x in range(len(bo)):
        for y in range(len(bo[0])):
            if bo[x][y] == 0:
                return (x, y)  # row, column

    return None


def is_valid(bo, num, pos):
    # Check row
    for x in range(len(bo[0])):
        if bo[pos[0]][x] == num and pos[1] != x:
            return False

    # Check column
    for y in range(len(bo)):
        if bo[y][pos[1]] == num and pos[0] != y:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for x in range(box_y*3, box_y*3 + 3):
        for y in range(box_x * 3, box_x*3 + 3):
            if bo[x][y] == num and (x,y) != pos:
                return False

    return True

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw strikes
    text = font.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw_board()


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    time_formatted = " " + str(minute) + ":" + str(sec)
    return time_formatted