from datetime import datetime, timedelta
import threading


# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

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

def loop_over_range(start_num, end_num):
      global prime_count;
      for i in range(start_num, end_num):
            if is_prime(i):
                  prime_count += 1

if __name__ == '__main__':
      log = Log(show_terminal=True)
      log.start_timer()

      start = 10_000_000_000
      range_count = 100_000
      threads = []

      # divide the range into 10 sets of equal size
      step = 10_000

      # create a thread for each set
      for num in range(start, start + range_count, step):
            end = num + step
            t = threading.Thread(target=loop_over_range, args=(num, end))
            threads.append(t)

      # start each thread
      for t in threads:
            t.start()
      for t in threads:
            t.join()

      # Should find 4306 primes
      log.write(f'Numbers processed = {numbers_processed}')
      log.write(f'Primes found      = {prime_count}')
      log.stop_timer('Total time')


