# Main, contains game setup/logic 

# I want the arrow keys to move the cursor as well as mouse

from Grid import Grid
from main_helpers import redraw_window
import time
import pygame


win = pygame.display.set_mode((540,600))
pygame.display.set_caption("Sudoku")
board = Grid(9, 9, 540, 540, win)
key = None
play = True
start = time.time()
strikes = 0
while play:

    play_time = round(time.time() - start)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                key = 1
            if event.key == pygame.K_2:
                key = 2
            if event.key == pygame.K_3:
                key = 3
            if event.key == pygame.K_4:
                key = 4
            if event.key == pygame.K_5:
                key = 5
            if event.key == pygame.K_6:
                key = 6
            if event.key == pygame.K_7:
                key = 7
            if event.key == pygame.K_8:
                key = 8
            if event.key == pygame.K_9:
                key = 9
            # Added for keypad
            if event.key == pygame.K_KP1:
                key = 1
            if event.key == pygame.K_KP2:
                key = 2
            if event.key == pygame.K_KP3:
                key = 3
            if event.key == pygame.K_KP4:
                key = 4
            if event.key == pygame.K_KP5:
                key = 5
            if event.key == pygame.K_KP6:
                key = 6
            if event.key == pygame.K_KP7:
                key = 7
            if event.key == pygame.K_KP8:
                key = 8
            if event.key == pygame.K_KP9:
                key = 9
            if event.key == pygame.K_BACKSPACE:
                board.clear_entry()
                key = None

            if event.key == pygame.K_RETURN:
                x, y = board.selected
                if board.boxes[x][y].temp != 0:
                    if board.place(board.boxes[x][y].temp):
                        print("Correct")
                    else:
                        print("Incorrect")
                        strikes += 1
                    key = None

                    if board.is_finished():
                        play_time = time.time() - start
                        print("Game over")
                        time.sleep(10)
                        play = False

            if event.key == pygame.K_SPACE:
                board.solve_board()
                play_time = time.time() - start
                print("Game over")
                time.sleep(10)
                play = False

            if event.key == pygame.K_ESCAPE:
                print("Game ended")
                play = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked = board.click(pos)
            if clicked:
                board.select(clicked[0], clicked[1])
                key = None

        if event.key == pygame.K_UP:
            board.arrows(pos, 'U')
        if event.key == pygame.K_DOWN:
            board.arrows(pos, 'D')
        if event.key == pygame.K_LEFT:
            board.arrows(pos, 'L')
        if event.key == pygame.K_RIGHT:
            board.arrows(pos, 'R')


    if board.selected and key != None:
        board.sketch_entry(key)

    redraw_window(win, board, play_time, strikes)
    pygame.display.update()
