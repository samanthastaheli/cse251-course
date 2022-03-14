"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: Samantha Staheli

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
import math
from multiprocessing.dummy import current_process
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 common Python files - Dont change
from cse251 import *
# set_working_directory(__file__)

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
DONE = False

# TODO add any functions

def solve_path(maze, position=None, path=None):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
    global DONE
    # TODO start add code here
    if position is None and path is None:
        position = maze.start_pos
        path = []
        
    
    row = position[0]
    col = position[1]
    moves = maze.get_possible_moves(row, col)

    if DONE == True:
        return
    else:
        if maze.at_end(row, col):
            DONE = True
        if len(moves) == 0:
            maze.restore(row, col)
            return
        else:
            for pos in moves:
                row = pos[0]
                col = pos[1]
                path.append(pos)
                maze.move(row, col, COLOR)
                position = (row, col)
                solve_path(maze, position, path)
    return path
    

def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()

