"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Samantha Staheli

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()

This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

To show a path to the end I would have 1 thread that moves based on the 
other threads. The other threads will have a Boolean argument that is 
true if the thread is still moving or false if it is stopped. If the 
argument is true the main thread that will show the correct path will 
follow that thread until the argument is false. Once the argument is 
false the main thread will backtrack and follow a different thread. 
It will do this until it finds the thread that is at the end. 

Why would it work?

It would work because the main thread does not have to try every move option.
Instead the other threads will do that. The other threads will have different 
colors until the main thread moves in that threads path, so the main thread 
will override the other threads colors to show the correct path.

"""
from asyncio import threads
import math
import threading
from turtle import position 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *
set_working_directory(__file__)

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def get_moves(maze, position):
    """ Call the get_possible_moves() function from Maze.
        Returns """
    row = position[0]
    col = position[1]
    moves = maze.get_possible_moves(row, col)
    return moves


def do_move(maze, position, color):
    """ Calls move method from Maze. """
    row = position[0]
    col = position[1]
    maze.move(row, col, color)
    # print(f'Moving... Color: {color} Cordinates: ({row}, {col})')


def solve_find_end(maze, position, color):
    """ finds the end position using threads. Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    # use at_end() or when 0 moves left
    global thread_count
    global stop

    row = position[0]
    col = position[1]
    # stop when end is reached
    if maze.at_end(row, col) or stop == True: 
        stop = True
        return

    moves = get_moves(maze, position)

    # if only 1 move, move and call solve_find_maze again with current color and position
    # make new thread and call function again
    if len(moves) == 0:
        return
    elif len(moves) == 1:
        # time.sleep(.5)
        pos = moves[0]
        do_move(maze, pos, color)
        solve_find_end(maze, pos, color)
    else:
        for pos in moves:
            if pos == moves[0]:
                do_move(maze, pos, color)
                thread = threading.Thread(target=solve_find_end, args=(maze, pos, color))
                thread_count += 1
                thread.start()
                # solve_find_end(maze, pos, color)
            else:
                color = get_color()
                do_move(maze, pos, color)
                thread = threading.Thread(target=solve_find_end, args=(maze, pos, color))
                thread_count += 1
                thread.start()
                # solve_find_end(maze, pos, color)
        thread.join()
        


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global stop
    stop = False

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)
    position = maze.get_start_pos()
    maze.move(position[0], position[1], COLOR)
    threads = []

    solve_find_end(maze, position, COLOR)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

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



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()