"""
Course: CSE 251
Lesson Week: 01 - Team Acvitiy
File: team.py
Author: Brother Comeau

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review team acvitiy details in I-Learn

"""

from datetime import datetime, timedelta
import threading


# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)
# https://github.com/byui-cse/cse251-course


# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0

def is_prime(n: int) -> bool:
    global numbers_processed
    numbers_processed += 1

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


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running DONE!
    # TODO 2) move the following for loop into 1 thread 
    # TODO 3) change the program to divide the for loop into 10 threads

    start = 10000000000
    range_count = 100000

    def try_find_primes(start, end):
        prime_count = 0
        for i in range(start, end):
            if is_prime(i):
                prime_count += 1
                print(i, end=', ', flush=True)

    # thread will execute is_prime() function or function with for loop in it 
    # thread arguments is the range of numbers 

    t = threading.Thread(target=try_find_primes, args=(start, start + range_count))
    print(flush=True)
    t.start()

    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')


