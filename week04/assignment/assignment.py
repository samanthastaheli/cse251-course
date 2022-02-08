"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: <Your name>
Purpose: Assignment 04 - Factory and Dealership
Instructions:
- See I-Learn

Submission comment:
My program meets all the requirements. I tried to make it 
my own by adding informative print statements and writiing to the log.
I did this to help me know what and when info was being used.
Also, I worked on this with my team.
"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'assembled: {self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        if len(self.items) == 0:
            print('!!! Cannot pop item because there is none !!!')
        else:
            return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self,
                 sem_high: threading.Semaphore,
                 sem_low: threading.Semaphore,
                 car_queue):
        # DONE, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.sem_high = sem_high
        self.sem_low = sem_low
        self.car_queue = car_queue
        self.cars_made = 0


    def run(self):
        for i in range(CARS_TO_PRODUCE):
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
            """
            # TODO Add you code here
            self.sem_high.acquire() # check to see if dealer is full

            self.car_queue.put(Car()) # appends car class to queue, a result of car class is added
            self.cars_made += 1

            self.sem_low.release()
            i += 1

        # signal the dealer that there there are not more cars
        # self.sem_high.acquire()
        if self.cars_made == CARS_TO_PRODUCE:
            self.car_queue.put(None)
            print('!!! No More Cars in Factory !!!')
        if(self.car_queue.size() > MAX_QUEUE_SIZE):
            print(f'!!! Dealer Overflow !!!')
        
        self.sem_low.release()

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self,
                 sem_high: threading.Semaphore,
                 sem_low: threading.Semaphore,
                 car_queue,
                 queue_stats):
        # DONE, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.sem_high = sem_high
        self.sem_low = sem_low
        self.car_queue = car_queue
        self.queue_stats = queue_stats

    def run(self):
        while True:
            # DONE Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            self.sem_low.acquire()

            car = self.car_queue.get()
            # check if done
            if(car == None):
                print('!!! No cars in Dealer !!!')
                break
            else:
                print(f'sold: {car.make} {car.model} {car.year}, queue size: {self.car_queue.size()}')

            self.queue_stats[self.car_queue.size()] += 1

            self.sem_high.release()
            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        self.sem_high.release()


def main():
    log = Log(show_terminal=True)

    # DONE Create semaphore(s)
    sem_high = threading.Semaphore(MAX_QUEUE_SIZE) # in, starts higher
    sem_low = threading.Semaphore(0) # out, starts lower than in semaphore 

    # DONE Create queue251 
    car_queue = Queue251()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # DONE create your one factory
    factory = Factory(sem_high, sem_low, car_queue)
    
    # DONE create your one dealership
    dealer = Dealer(sem_high, sem_low, car_queue, queue_stats)

    log.start_timer()

    # DONE Start factory and dealership
    factory.start()
    dealer.start()

    factory.join()
    dealer.join()
    
    # DONE Wait for factory and dealership to complete

    log.stop_timer(f'All {sum(queue_stats)} have been created')
    log.write(f'sleep reduce factor was: {SLEEP_REDUCE_FACTOR}')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')

if __name__ == '__main__':
    main()