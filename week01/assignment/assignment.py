"""
Course: CSE 251 
Lesson Week: 01
File: assignment.py 
Author: <Add name here>

Purpose: Drawing with Python Turtle

The follow program will draw a series of shapes - squares, circles, triangles
and rectangles.  

There is a Python class called cse251Turtle that is used to hold the drawing
commands that are created by the program.  This is required because threads can
not draw to the screen - only the main thread can do this.

Instructions:

- Find the "TODO" comment below and add your code that will use threads.
- You are not allowed to use any other Python modules/packages than the packages
  currently imported below.
- You can create other functions if needed.
- No global variables.

Justification Statement:
I think my code meets requirements. However, if the requirment was to draw a random 
number of shapes at a time then I would be slightly deficiant. I was confused by the 
direction that some not all shapes are supposed to be drawn.

"""


import math
import threading 
from cse251turtle import *

# Include CSE 251 common Python files. 
from cse251 import *
set_working_directory(__file__)


def draw_square(tur, x, y, side, color='black'):
    """Draw Square"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    for _ in range(4):
        tur.forward(side)
        tur.right(90)


def draw_circle(tur, x, y, radius, color='red'):
    """Draw Circle"""
    steps = 8
    circumference = 2 * math.pi * radius

    # Need to adjust starting position so that (x, y) is the center
    x1 = x - (circumference // steps) // 2
    y1 = y
    tur.move(x1 , y1 + radius)

    tur.setheading(0)
    tur.color(color)
    for _ in range(steps):
        tur.forward(circumference / steps)
        tur.right(360 / steps)


def draw_rectangle(tur, x, y, width, height, color='blue'):
    """Draw a rectangle"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    tur.forward(width)
    tur.right(90)
    tur.forward(height)
    tur.right(90)
    tur.forward(width)
    tur.right(90)
    tur.forward(height)
    tur.right(90)


def draw_triangle(tur, x, y, side, color='green'):
    """Draw a triangle"""
    tur.move(x, y)
    tur.setheading(0)
    tur.color(color)
    for _ in range(4):
        tur.forward(side)
        tur.left(120)


def draw_coord_system(tur, x, y, size=300, color='black'):
    """Draw corrdinate lines"""
    tur.move(x, y)
    for i in range(4):
        tur.forward(size)
        tur.backward(size)
        tur.left(90)

def draw_squares(tur):
    """Draw a group of squares"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_square(tur, x - 50, y + 50, 100)


def draw_circles(tur):
    """Draw a group of circles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_circle(tur, x, y-2, 50)


def draw_triangles(tur):
    """Draw a group of triangles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_triangle(tur, x-30, y-30+10, 60)


def draw_rectangles(tur):
    """Draw a group of Rectangles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            draw_rectangle(tur, x-10, y+5, 20, 15)

def draw_thread_squares(tur, lock):
    """Draw a group of squares"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            lock.aquire()
            draw_square(tur, x - 50, y + 50, 100)
            lock.release()

def draw_thread_circles(tur, lock):
    """Draw a group of circles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            lock.aquire()
            draw_circle(tur, x, y-2, 50)
            lock.release()

def draw_thread_triangles(tur, lock):
    """Draw a group of triangles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            lock.aquire()
            draw_triangle(tur, x-30, y-30+10, 60)
            lock.release()

def draw_thread_rectangles(tur, lock):
    """Draw a group of Rectangles"""
    for x in range(-300, 350, 200):
        for y in range(-300, 350, 200):
            lock.aquire()
            draw_rectangle(tur, x-10, y+5, 20, 15)
            lock.release()

def run_no_threads(tur, log, main_turtle):
    """Draw different shapes without using threads"""

    # Draw Coords system
    tur.pensize(0.5)
    draw_coord_system(tur, 0, 0, size=375)
    tur.pensize(4)

    log.write('-' * 50)
    log.start_timer('Start Drawing No Threads')
    tur.move(0, 0)

    draw_squares(tur)
    draw_circles(tur)
    draw_triangles(tur)
    draw_rectangles(tur)

    log.step_timer('All drawing commands have been created')

    tur.move(0, 0)
    log.write(f'Number of Drawing Commands: {tur.get_command_count()}')

    # Play the drawing commands that were created
    tur.play_commands(main_turtle)
    log.stop_timer('Total drawing time')
    tur.clear()

def run_with_threads(tur, log, main_turtle):
    """Draw different shapes using threads"""

    # Draw Coors system
    tur.pensize(0.5)
    draw_coord_system(tur, 0, 0, size=375)
    tur.pensize(4)
    log.write('-' * 50)
    log.start_timer('Start Drawing With Threads')

    # TODO - Start add your code here.
    # You need to use 4 threads where each thread concurrently drawing one type of shape.
    # You are free to change any functions in this code except main()
    """Draw using lock"""

    lock = threading.Lock()

    tur.move(0, 0)
    thread_rec = threading.Thread(draw_rectangle(tur, lock))
    thread_cir = threading.Thread(draw_circle(tur, lock))
    thread_sq = threading.Thread(draw_square(tur, lock))
    thread_tri = threading.Thread(draw_triangle(tur, lock))

    thread_rec.start()
    thread_cir.start()
    thread_sq.start()
    thread_tri.start()
    
    thread_rec.join()
    thread_cir.join()
    thread_sq.join()
    thread_tri.join()

    """test 5: lock"""
    # lock = threading.Lock()
    # lock.acquire()
    # thread_rec = threading.Thread(draw_rectangles(tur))
    # thread_rec = open('CSE251Turtle.py')
    # thread_rec.write("2")
    # thread_rec.close()
    # lock.release()


    """test 4"""
    # for a in range(-300, 350, 200):
    #     for b in range(-300, 350, 200):
    #         thread_rec = threading.Thread(draw_rectangle(tur, a-10, b+5, 20, 15))
    #         thread_rec.start()
    #         thread_rec.join()

    #         for c in range(-300, 350, 200):
    #             for d in range(-300, 350, 200):
    #                 thread_cir = threading.Thread(draw_circle(tur, c, d-2, 50))
    #                 thread_cir.start()
    #                 thread_cir.join()

    #             for e in range(-300, 350, 200):
    #                 for f in range(-300, 350, 200):
    #                     thread_sq = threading.Thread(draw_square(tur, e - 50, f + 50, 100))
    #                     thread_sq.start()
    #                     thread_sq.join()

    #                 for g in range(-300, 350, 200):
    #                     for h in range(-300, 350, 200):
    #                         thread_tri = threading.Thread(draw_triangle(tur, g-30, h-30+10, 60))
    #                         thread_tri.start()
    #                         thread_tri.join()
    
    """test 3"""
    # for x in range(-300, 350, 200):
    #     for y in range(-300, 350, 200):
    #         thread_rec = threading.Thread(draw_rectangle(tur, x-10, y+5, 20, 15))
    #         thread_rec.start()
    #         thread_rec.join()

    # for x in range(-300, 350, 200):
    #     for y in range(-300, 350, 200):
    #         thread_cir = threading.Thread(draw_circle(tur, x, y-2, 50))
    #         thread_cir.start()
    #         thread_cir.join()

    # for x in range(-300, 350, 200):
    #     for y in range(-300, 350, 200):
    #         thread_sq = threading.Thread(draw_square(tur, x - 50, y + 50, 100))
    #         thread_sq.start()
    #         thread_sq.join()

    # for x in range(-300, 350, 200):
    #     for y in range(-300, 350, 200):
    #         thread_tri = threading.Thread(draw_triangle(tur, x-30, y-30+10, 60))
    #         thread_tri.start()
    #         thread_tri.join()

    """test 2"""
    # for x in range(-300, 350, 200):
    #     for y in range(-300, 350, 200):
    #         thread_rec = threading.Thread(draw_rectangle(tur, x-10, y+5, 20, 15))
    #         thread_cir = threading.Thread(draw_circle(tur, x, y-2, 50))
    #         thread_sq = threading.Thread(draw_square(tur, x - 50, y + 50, 100))
    #         thread_tri = threading.Thread(draw_triangle(tur, x-30, y-30+10, 60))

    #         thread_rec.start()
    #         thread_cir.start()
    #         thread_sq.start()
    #         thread_tri.start()
            
    #         thread_rec.join()
    #         thread_cir.join()
    #         thread_sq.join()
    #         thread_tri.join()

    """test 1"""
    # thread_rec = threading.Thread(draw_rectangles(tur))
    # thread_cir = threading.Thread(draw_circles(tur))
    # thread_sq = threading.Thread(draw_squares(tur))
    # thread_tri = threading.Thread(draw_triangles(tur))

    # thread_rec.start()
    # thread_cir.start()
    # thread_sq.start()
    # thread_tri.start()
    
    # thread_rec.join()
    # thread_cir.join()
    # thread_sq.join()
    # thread_tri.join()
    
    log.step_timer('All drawing commands have been created')

    log.write(f'Number of Drawing Commands: {tur.get_command_count()}')

    # Play the drawing commands that were created
    tur.play_commands(main_turtle)
    log.stop_timer('Total drawing time')
    tur.clear()


def main():
    """Main function - DO NOT CHANGE"""

    log = Log(show_terminal=True)

    # create a Screen Object
    screen = turtle.Screen()

    # Screen configuration
    screen.setup(800, 800)

    # Make turtle Object
    main_turtle = turtle.Turtle()
    main_turtle.speed(0)

    # Special CSE 251 Turtle Class
    turtle251 = CSE251Turtle()

    # Test 1 - Drawing with no threads
    run_no_threads(turtle251, log, main_turtle)
    
    main_turtle.clear()

    # Test 2 - Drawing with threads
    run_with_threads(turtle251, log, main_turtle)

    # Waiting for user to close window
    turtle.done()


if __name__ == "__main__":
    main()
