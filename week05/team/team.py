"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread/process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random

#Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

PRIME_PROCESS_COUNT = 3

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# TODO create read_thread function
def read_thread(queue:mp.Queue, filename):
    file = open(filename, "r")
    for i in file:
        queue.put(i)


# TODO create prime_process function
def prime_process(queue:mp.Queue, shared_list):
    while not queue.empty():
        number = int(queue.get())
        check = is_prime(number)
        if check == True:
            shared_list.append(number)
    


def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    # create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    queue = mp.Queue()
    primes = mp.Manager().list()

    # TODO create reading thread
    reading = threading.Thread(target=read_thread, args=(queue, filename))

    # TODO create prime processes
    prime_p = [mp.Process(target=prime_process, args=(queue, primes)) for _ in range(PRIME_PROCESS_COUNT)]

    # TODO Start them all
    reading.start()
    for i in range(PRIME_PROCESS_COUNT):
        prime_p[i].start()

    # TODO wait for them to complete
    reading.join()
    for i in range(PRIME_PROCESS_COUNT):
        prime_p[i].join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()