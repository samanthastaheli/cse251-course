"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: Samantha Staheli

Purpose: Assignment 05 - Factories and Dealers

Submisson Commment:
I am slightly deficient.
My factory and dealer's make and sell the cars, but my code does not produce a log. 

"""

from datetime import datetime, timedelta
import multiprocessing
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 5000

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

        # Display the car that has was just created in the terminal
        self.display()
           
    def display(self):
        print(f'assembled: {self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        if len(self.items) == 0:
            print('!!! Cannot pop item because there is none !!!')
        else:
            return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self,
                 factory_id,
                 sem_high: threading.Semaphore,
                 sem_low: threading.Semaphore,
                 car_queue, 
                 factory_stats,
                 barrier):
        self.cars_to_produce = random.randint(100, 200)     # Don't change, og 200, 300
        
        threading.Thread.__init__(self)
        self.sem_high = sem_high
        self.sem_low = sem_low
        self.car_queue = car_queue
        self.cars_made = 0 # not being used yet, don't know if need to keep track of this
        self.factory_stats = factory_stats
        self.barrier = barrier
        self.factory_id = factory_id

    def run(self):
        for i in range(self.cars_to_produce):
            # print(f'running factory for the {i} time')
            # if (self.factory_id == 0):
            #     self.sem_high.acquire()
            #     self.car_queue.put(None)
            #     self.sem_low.release()
            
            # TODO produce the cars, then send them to the dealerships
            self.sem_high.acquire()
            self.car_queue.put(Car()) # appends car class to queue, a result of car class is added
            self.factory_stats[self.factory_id] += 1 
            # TODO wait until all of the factories are finished producing cars
            self.barrier.wait()
            self.sem_low.release()
        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        self.sem_low.release()
        
            

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, 
                 dealer_id,
                 sem_high: threading.Semaphore,
                 sem_low: threading.Semaphore,
                 car_queue,
                 dealer_stats,
                 dealer_barrier):
        threading.Thread.__init__(self)
        self.sem_high = sem_high
        self.sem_low = sem_low
        self.car_queue = car_queue
        self.dealer_stats = dealer_stats
        self.dealer_id = dealer_id
        self.dealer_barrier = dealer_barrier

    def run(self):
        while True:
            # print('running dealer')
            # TODO handle a car
            self.sem_low.acquire()

            car = self.car_queue.get()
            
            if(car == None): # check if done
                print('!!! No cars in Dealer !!!')
                break
            else:
                print(f'sold: {car.make} {car.model} {car.year}')

            self.dealer_stats[self.dealer_id] += 1
            self.dealer_barrier.wait()
            self.sem_high.release()
            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))
        

        
def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """
    print('production started')
    # DONE Create semaphore(s)
    sem_high = threading.Semaphore(MAX_QUEUE_SIZE) # in, starts higher
    sem_low = threading.Semaphore(0) # out, starts lower than in semaphore 

    # DONE Create queue
    car_queue = Queue251()

    # TODO Create lock(s)
    # ??? do i need locks ???

    # TODO Create barrier(s)
    # ??? need to pass in number of cars to create per factory 
    # so need to make barrier in factory class
    # barrier = multiprocessing.Barrier(MAX_QUEUE_SIZE)
    factory_barrier = multiprocessing.Barrier(factory_count)
    dealer_barrier = multiprocessing.Barrier(dealer_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)

    # this tracks number of factories there are
    factory_stats = list([0] * factory_count)

    # DONE create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factories = []
    for i in range(factory_count): 
        factories.append(Factory(i, sem_high, sem_low, car_queue, factory_stats, factory_barrier))
        # factories.append(multiprocessing.Process(target=Factory, args=(i, sem_high, sem_low, car_queue, factory_stats, factory_barrier)))

    # factory_barrier.wait() # fill queue before going to dealer

    # DONE create your dealerships
    dealers = []
    for i in range(dealer_count):
        dealers.append(Dealer(i, sem_high, sem_low, car_queue, dealer_stats, dealer_barrier))
        # dealers.append(multiprocessing.Process(target=Dealer, args=(i, sem_high, sem_low, car_queue, dealer_stats)))

    log.start_timer()

    # DONE Start all factories
    for factory in factories:
        factory.start()

    # DONE Start all dealerships
    for dealer in dealers:
        dealer.start()
    
    time.sleep(1)   # make sure all dealers have time to start

    # DONE Wait for factories and dealerships to complete (join)
    # for i in range(dealer_count):
    #     dealers[i].join()
    # for i in range(factory_count):
    #     factories[i].join()
    for factory in factories:
        factory.join()
    for dealer in dealers:
        dealer.join()
    
    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factor Stats   : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)
# def main(log):
#     """ Main function - THAT IS CHANGED for test purposes! """
#     factories = 1
#     dealerships = 1
#     run_production(factories, dealerships)

#     log.write(f'Factories      : {factories}')
#     log.write(f'Dealerships    : {dealerships}')
#     # log.write(f'Run Time       : {run_time:.4f}')
#     # log.write(f'Max queue size : {max_queue_size}')
#     # log.write(f'Factor Stats   : {factory_stats}')
#     # log.write(f'Dealer Stats   : {dealer_stats}')
#     log.write('')

#     # The number of cars produces needs to match the cars sold
#     # assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':
    log = Log(show_terminal=True)
    main(log)


