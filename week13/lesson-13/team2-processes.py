from cse251 import *
from datetime import datetime, timedelta
import multiprocessing

from numpy import longlong


def is_prime(n: longlong):

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


def loop_over_range(start_num, end_num, primes, numbers_processed, lock):
    for i in range(start_num, end_num):
        #print(f'{i=}')
        with lock:
            numbers_processed.value += 1
        if is_prime(i):
            #print(f'{i} is prime')
            with lock:
                primes.value += 1


if __name__ == '__main__':
    start_time = time.time()
    start = 10_000_000_000
    range_count = 100_000
    processes = []

    # divide the range into 10 sets of equal size
    step = 10_000

    primes = multiprocessing.Value("i", 0)
    numbers_processed = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()

    # create a thread for each set
    for num in range(start, start + range_count, step):
        end = num + step
        p = multiprocessing.Process(
            target=loop_over_range, args=(num, end, primes, numbers_processed, lock))
        processes.append(p)

    # start each thread
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    # Should find 4306 primes
    print(f'Numbers processed = {numbers_processed.value}')
    print(f'Primes found      = {primes.value}')
    print(f'Total time = {time.time() - start_time}')
